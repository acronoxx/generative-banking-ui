// Agent de l'essai AI SDK UI : ToolLoopAgent avec les outils bancaires et un
// outil de virement soumis à l'approbation de l'utilisateur (needsApproval).
// Il est servi par server.ts et utilisé par les pages genui-ai-sdk et assistant-ui.

import { ToolLoopAgent, tool, type InferAgentUIMessage } from "ai";
import { createGoogleGenerativeAI } from "@ai-sdk/google";
import { z } from "zod";

// Le fournisseur lit par défaut GOOGLE_GENERATIVE_AI_API_KEY : on lui passe la clé commune
const google = createGoogleGenerativeAI({ apiKey: process.env.GOOGLE_API_KEY });

const TRANSACTIONS = [
  { libelle: "Loyer", montant: 780 },
  { libelle: "Garage", montant: 620 },
  { libelle: "Courses", montant: 95 },
  { libelle: "Billets de train", montant: 510 },
];

export const agent = new ToolLoopAgent({
  // Modèle des essais par défaut ; GEMINI_MODEL permet d'en changer (quota épuisé, par exemple)
  model: google(process.env.GEMINI_MODEL ?? "gemini-3.5-flash-lite"),
  instructions:
    "Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données. " +
    "Les résultats des outils sont déjà affichés à l'utilisateur sous forme de cartes : ne les recopie pas.",
  tools: {
    get_balance: tool({
      description: "Renvoie le solde d'un compte ('courant' ou 'livret').",
      inputSchema: z.object({ account: z.enum(["courant", "livret"]) }),
      execute: async ({ account }) => ({ compte: account, solde: account === "courant" ? 1250 : 8400 }),
    }),
    get_transactions: tool({
      description: "Renvoie les transactions des trois derniers mois supérieures à un montant en euros.",
      inputSchema: z.object({ min_amount: z.number() }),
      execute: async ({ min_amount }) => TRANSACTIONS.filter((t) => t.montant >= min_amount),
    }),
    prepare_transfer: tool({
      description: "Effectue un virement d'un montant en euros vers un bénéficiaire.",
      inputSchema: z.object({ amount: z.number(), beneficiary: z.string() }),
      // Exécution suspendue jusqu'à ce que l'utilisateur approuve ou refuse dans l'interface
      needsApproval: true,
      execute: async ({ amount, beneficiary }) => ({ statut: "simulé", amount, beneficiary }),
    }),
  },
});

// Type des messages, partagé avec l'interface pour typer les parties « outil »
export type MessageBanque = InferAgentUIMessage<typeof agent>;
