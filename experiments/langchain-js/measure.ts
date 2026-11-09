// Mesure du framework LangChain.js selon le protocole commun (voir README.md) :
// même agent bancaire (gemini-3.5-flash-lite, outils get_balance et get_transactions),
// 4 scénarios répétés 10 fois. Affiche une ligne CSV par scénario.
// Lancement : node measure.ts

import "dotenv/config";
import { AIMessage, createAgent, tool } from "langchain";
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { z } from "zod";

const FRAMEWORK = "LangChain.js";
const REPETITIONS = 10;
const PAUSE = 10; // secondes entre deux essais, pour respecter le quota gratuit

const getBalance = tool(
  async ({ account }) => {
    const soldes: Record<string, string> = { courant: "1 250 €", livret: "8 400 €" };
    return soldes[account] ?? "Compte inconnu";
  },
  {
    name: "get_balance",
    description: "Renvoie le solde d'un compte ('courant' ou 'livret').",
    schema: z.object({ account: z.string() }),
  },
);

const getTransactions = tool(
  async ({ min_amount }) => {
    const transactions: [string, number][] = [["Loyer", 780], ["Garage", 620], ["Courses", 95], ["Billets de train", 510]];
    const resultat = transactions.filter(([, montant]) => montant >= min_amount).map(([nom, montant]) => `${nom} : ${montant} €`);
    return resultat.join("\n") || "Aucune transaction";
  },
  {
    name: "get_transactions",
    description: "Renvoie les transactions des trois derniers mois supérieures à un montant en euros.",
    schema: z.object({ min_amount: z.number() }),
  },
);

// Chaque scénario : une question et les outils qui doivent être appelés
const SCENARIOS: [string, string[]][] = [
  ["Quel est le solde de mon compte courant ?", ["get_balance"]],
  ["Quelles dépenses dépassent 500 € ?", ["get_transactions"]],
  ["Quel est mon solde courant, et quelles dépenses dépassent 500 € ?", ["get_balance", "get_transactions"]],
  ["Bonjour, que peux-tu faire pour moi ?", []],
];

// La clé est lue dans GOOGLE_API_KEY
const model = new ChatGoogleGenerativeAI({ model: "gemini-3.5-flash-lite", maxRetries: 0 });
const agent = createAgent({
  model,
  tools: [getBalance, getTransactions],
  systemPrompt: "Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
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
    let result;
    try {
      // Délai maximal de 60 s pour l'ensemble de l'exécution
      result = await agent.invoke(
        { messages: [{ role: "user", content: question }] },
        { signal: AbortSignal.timeout(60_000) },
      );
    } catch (erreur: any) {
      console.log(`  essai en échec : ${erreur?.name} : ${String(erreur?.message).slice(0, 200)}`);
      await pause(PAUSE);
      continue;
    }
    durees.push((performance.now() - debut) / 1000);

    const reponses = result.messages.filter(AIMessage.isInstance);
    const outilsAppeles = new Set(reponses.flatMap((m) => m.tool_calls ?? []).map((appel) => appel.name));

    appels.push(reponses.length);
    entrees.push(reponses.reduce((t, m) => t + (m.usage_metadata?.input_tokens ?? 0), 0));
    sorties.push(reponses.reduce((t, m) => t + (m.usage_metadata?.output_tokens ?? 0), 0));
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
