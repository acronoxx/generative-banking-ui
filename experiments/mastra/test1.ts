// Premier essai Mastra : agent avec les deux outils bancaires, avant le script de mesure.

import "dotenv/config";
import { Agent } from "@mastra/core/agent";
import { createTool } from "@mastra/core/tools";
import { z } from "zod";

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

const agent = new Agent({
  id: "assistant-bancaire",
  name: "Assistant bancaire",
  instructions: "Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
  model: "google/gemini-3.5-flash-lite",
  tools: { get_balance: getBalance, get_transactions: getTransactions },
});

console.log("Envoi de la question...");

const response = await agent.generate("Quel est mon solde courant, et quelles dépenses dépassent 500 € ?");

response.steps.forEach((step: any, i: number) => {
  console.log(`\n===== Étape ${i + 1} =====`);
  for (const appel of step.toolCalls ?? []) {
    const p = appel.payload ?? appel;
    console.log("Appel d'outil :", p.toolName, JSON.stringify(p.args));
  }
  for (const res of step.toolResults ?? []) {
    const p = res.payload ?? res;
    console.log("Résultat :", p.toolName, "->", p.result);
  }
  if (step.text) console.log("Texte :", step.text);
});

console.log("\nRéponse finale :");
console.log(response.text);