// Outils de la page : définis une seule fois, ils sont déclarés au navigateur
// avec WebMCP et transmis à l'agent, qui les appelle par function calling.

import { z } from "zod";

const API = "http://127.0.0.1:8000/api";

export const consulterComptes = {
  name: "consulter_comptes",
  description: "Renvoie la liste des comptes de l'utilisateur avec leur solde.",
  parameters: z.object({}),
  handler: async () => (await fetch(`${API}/comptes`)).json(),
};

export const consulterTransactions = {
  name: "consulter_transactions",
  description: "Renvoie les transactions des trois derniers mois supérieures à un montant en euros.",
  parameters: z.object({ min_amount: z.number().describe("Montant minimal en euros") }),
  handler: async ({ min_amount }: { min_amount: number }) =>
    (await fetch(`${API}/transactions?min_amount=${min_amount}`)).json(),
};

export const OUTILS = [consulterComptes, consulterTransactions];
