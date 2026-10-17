// Mesure du framework Mastra selon le protocole commun (voir README.md) :
// même agent bancaire (gemini-3.5-flash-lite, outils get_balance et get_transactions),
// 4 scénarios répétés 10 fois. Affiche une ligne CSV par scénario.
// Lancement : node measure.ts

import "dotenv/config";
import { Agent } from "@mastra/core/agent";
import { createTool } from "@mastra/core/tools";
import { z } from "zod";

const FRAMEWORK = "Mastra";
const REPETITIONS = 10;
const PAUSE = 10; // secondes entre deux essais, pour respecter le quota gratuit

const getBalance = createTool({
  id: "get_balance",
  description: "Renvoie le solde d'un compte ('courant' ou 'livret').",
  inputSchema: z.object({ account: z.string() }),
  execute: async ({ account }) => {
    const soldes: Record<string, string> = { courant: "1 250 €", livret: "8 400 €" };
    return soldes[account] ?? "Compte inconnu";
  },
});

const getTransactions = createTool({
  id: "get_transactions",
  description: "Renvoie les transactions des trois derniers mois supérieures à un montant en euros.",
  inputSchema: z.object({ min_amount: z.number() }),
  execute: async ({ min_amount }) => {
    const transactions: [string, number][] = [["Loyer", 780], ["Garage", 620], ["Courses", 95], ["Billets de train", 510]];
    const resultat = transactions.filter(([, montant]) => montant >= min_amount).map(([nom, montant]) => `${nom} : ${montant} €`);
    return resultat.join("\n") || "Aucune transaction";
  },
});

// Chaque scénario : une question et les outils qui doivent être appelés
const SCENARIOS: [string, string[]][] = [
  ["Quel est le solde de mon compte courant ?", ["get_balance"]],
  ["Quelles dépenses dépassent 500 € ?", ["get_transactions"]],
  ["Quel est mon solde courant, et quelles dépenses dépassent 500 € ?", ["get_balance", "get_transactions"]],
  ["Bonjour, que peux-tu faire pour moi ?", []],
];

const agent = new Agent({
  id: "assistant-bancaire",
  name: "Assistant bancaire",
  instructions: "Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
  model: "google/gemini-3.5-flash-lite",
  tools: { get_balance: getBalance, get_transactions: getTransactions },
});

const pause = (s: number) => new Promise((r) => setTimeout(r, s * 1000));
const mediane = (v: number[]) => {
  const t = [...v].sort((a, b) => a - b);
  const m = Math.floor(t.length / 2);
  return t.length % 2 ? t[m] : (t[m - 1] + t[m]) / 2;
};

console.log("framework;question;duree_mediane_s;duree_min_s;duree_max_s;appels_modele;tokens_entree;tokens_sortie;reussite;erreurs");

for (const [question, outilsAttendus] of SCENARIOS) {
  const durees: number[] = [], appels: number[] = [], entrees: number[] = [], sorties: number[] = [];
  let reussites = 0;

  for (let i = 0; i < REPETITIONS; i++) {
    const debut = performance.now();
    let response: any;
    try {
      response = await agent.generate(question);
    } catch (erreur: any) {
      console.log(`  essai en échec : ${erreur?.name} : ${String(erreur?.message).slice(0, 200)}`);
      await pause(PAUSE);
      continue;
    }
    durees.push((performance.now() - debut) / 1000);

    const steps: any[] = response.steps ?? [];
    const outilsAppeles = new Set<string>(
      steps.flatMap((s) => s.toolCalls ?? []).map((a: any) => a.payload?.toolName ?? a.toolName),
    );
    const usage = steps.map((s) => s.usage ?? {});

    appels.push(steps.length);
    entrees.push(usage.reduce((t, u) => t + (u.inputTokens ?? u.promptTokens ?? 0), 0));
    sorties.push(usage.reduce((t, u) => t + (u.outputTokens ?? u.completionTokens ?? 0), 0));
    if (outilsAppeles.size === outilsAttendus.length && outilsAttendus.every((o) => outilsAppeles.has(o))) reussites++;
    await pause(PAUSE);
  }

  if (durees.length) {
    console.log(
      `${FRAMEWORK};${question};${mediane(durees).toFixed(2)};${Math.min(...durees).toFixed(2)};${Math.max(...durees).toFixed(2)};` +
        `${mediane(appels).toFixed(0)};${mediane(entrees).toFixed(0)};${mediane(sorties).toFixed(0)};` +
        `${reussites}/${durees.length};${REPETITIONS - durees.length}`,
    );
  }
}
