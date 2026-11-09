// Serveur de l'agent : le modèle reçoit la consigne générée par OpenUI à partir
// du catalogue, appelle les outils, puis répond en OpenUI Lang. Le texte est
// renvoyé en flux à la page, qui l'affiche au fur et à mesure.
// Le modèle est appelé directement chez Google, sans la passerelle de Thesys.
import "dotenv/config";
import { readFileSync } from "node:fs";
import { createServer } from "node:http";
import { createGoogleGenerativeAI } from "@ai-sdk/google";
import { createParser, generateSystemPrompt, type LibrarySpec } from "@openuidev/lang-core";
import { stepCountIs, streamText, tool } from "ai";
import { z } from "zod";

const PORT = 4200;

// Spécification du catalogue, produite par `npm run spec`
const spec = JSON.parse(readFileSync("generated/system-prompt.spec.json", "utf8")) as LibrarySpec;
const consigne = generateSystemPrompt({
  library: spec,
  promptOptions: {
    preamble:
      "Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données. " +
      "Réponds en français.",
    additionalRules: [
      "Pour un virement, n'appelle jamais execute_transfer avant que l'utilisateur ait confirmé " +
        "explicitement : affiche d'abord ConfirmationVirement.",
    ],
  },
});
const parseur = createParser(spec.schema!, spec.root);

const google = createGoogleGenerativeAI({ apiKey: process.env.GOOGLE_API_KEY });

const TRANSACTIONS = [
  { libelle: "Loyer", montant: 780 },
  { libelle: "Garage", montant: 620 },
  { libelle: "Courses", montant: 95 },
  { libelle: "Billets de train", montant: 510 },
];

const outils = {
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
  execute_transfer: tool({
    description: "Exécute un virement déjà confirmé par l'utilisateur.",
    inputSchema: z.object({ amount: z.number(), beneficiary: z.string() }),
    execute: async ({ amount, beneficiary }) => ({ statut: "simulé", amount, beneficiary }),
  }),
};

createServer(async (req, res) => {
  if (req.method !== "POST" || req.url !== "/api/chat") {
    res.writeHead(404).end();
    return;
  }
  let corps = "";
  for await (const morceau of req) corps += morceau;

  try {
    const { messages } = JSON.parse(corps);
    const resultat = streamText({
      model: google(process.env.GEMINI_MODEL ?? "gemini-3.5-flash-lite"),
      system: consigne,
      messages,
      tools: outils,
      stopWhen: stepCountIs(5),
      onFinish: ({ text, totalUsage, steps }) => {
        // Validation de la réponse par le parseur OpenUI : composants inconnus,
        // propriétés manquantes, références non définies ou orphelines
        const { root, meta } = parseur.parse(text);
        const appels = steps.flatMap((s) => s.toolCalls.map((c) => c.toolName));
        console.log(
          JSON.stringify({
            outils: appels,
            tokens_entree: totalUsage.inputTokens,
            tokens_sortie: totalUsage.outputTokens,
            caracteres: text.length,
            valide: root !== null && !meta.incomplete && meta.errors.length === 0 &&
              meta.unresolved.length === 0 && meta.orphaned.length === 0,
            erreurs: meta.errors,
            non_resolues: meta.unresolved,
            orphelines: meta.orphaned,
          }),
        );
        console.log(text);
      },
    });
    resultat.pipeTextStreamToResponse(res);
  } catch (erreur) {
    console.error(erreur);
    if (!res.headersSent) res.writeHead(500).end(String(erreur));
  }
}).listen(PORT, () => console.log(`Agent prêt sur http://localhost:${PORT}/api/chat`));
