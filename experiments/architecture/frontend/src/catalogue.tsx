// Catalogue A2UI de la page : les composants de base (Text, Card, Column…)
// plus quelques composants bancaires. Le schéma de chaque composant est envoyé
// à l'agent, qui compose l'interface avec ; la page les rend avec React.

import {
  type CatalogDefinitions,
  type ComponentRenderer,
  DynamicStringSchema,
  createCatalog,
  filterCatalog,
} from "@copilotkit/a2ui-renderer";
// Le moteur de rendu A2UI s'appuie sur l'API zod 3
import { z } from "zod/v3";

export const CATALOGUE_ID = "copilotkit://banque";

// zod/v3 et le zod 3 du moteur de rendu sont deux copies distinctes pour TypeScript
// (identiques à l'exécution) : les schémas sont convertis au type attendu, et les
// props des composants sont typées à la main.
const objet = (forme: Record<string, unknown>) =>
  z.object(forme as z.ZodRawShape) as unknown as CatalogDefinitions[string]["props"];

const definitions: CatalogDefinitions = {
  SoldeCompte: {
    description: "Tuile affichant un compte bancaire et son solde.",
    props: objet({
      nom: DynamicStringSchema.describe("Nom du compte, par exemple « Compte courant »"),
      solde: DynamicStringSchema.describe("Solde formaté, par exemple « 1 250 € »"),
    }),
  },
  Transaction: {
    description: "Ligne d'une transaction : libellé à gauche, montant à droite.",
    props: objet({
      libelle: DynamicStringSchema.describe("Libellé de la transaction"),
      montant: DynamicStringSchema.describe("Montant formaté, par exemple « 780 € »"),
    }),
  },
  Alerte: {
    description: "Bandeau de message mis en évidence (information ou avertissement).",
    props: objet({
      message: DynamicStringSchema.describe("Texte du message"),
      niveau: z.enum(["info", "attention"]).describe("info : bleu, attention : orange"),
    }),
  },
};

const COULEURS = { info: "#1d4ed8", attention: "#c2410c" };

const rendus: Record<string, ComponentRenderer<any>> = {
  SoldeCompte: ({ props }: { props: { nom: string; solde: string } }) => (
    <div style={{ padding: 16, borderRadius: 12, background: "#0f766e", color: "#fff", minWidth: 180 }}>
      <div style={{ fontSize: 13, opacity: 0.85 }}>{props.nom}</div>
      <div style={{ fontSize: 24, fontWeight: 600, marginTop: 4 }}>{props.solde}</div>
    </div>
  ),
  Transaction: ({ props }: { props: { libelle: string; montant: string } }) => (
    <div style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px solid #e5e7eb" }}>
      <span>{props.libelle}</span>
      <span style={{ fontWeight: 600, color: "#b91c1c" }}>− {props.montant}</span>
    </div>
  ),
  Alerte: ({ props }: { props: { message: string; niveau: keyof typeof COULEURS } }) => (
    <div
      style={{
        padding: "10px 14px",
        borderRadius: 8,
        borderLeft: `4px solid ${COULEURS[props.niveau]}`,
        background: "#f8fafc",
        color: COULEURS[props.niveau],
      }}
    >
      {props.message}
    </div>
  ),
};

// Composants de base conservés : la mise en page suffit, et le schéma de chaque
// composant est ajouté au prompt de l'agent (le catalogue complet pèse ~54 Ko)
const BASE = ["Column", "Row", "Card", "List", "Text", "Divider"];

export const catalogue = filterCatalog(
  createCatalog(definitions, rendus, { catalogId: CATALOGUE_ID, includeBasicCatalog: true }),
  (nom) => BASE.includes(nom) || nom in definitions,
);
