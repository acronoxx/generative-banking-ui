// Catalogue de composants bancaires : le modèle ne peut composer l'interface
// qu'avec ces composants, décrits par un schéma Zod de leurs propriétés.

import { createLibrary, defineComponent, useTriggerAction } from "@openuidev/react-lang";
import { z } from "zod/v4";

const carte = { border: "1px solid #d0d7de", borderRadius: 8, padding: 12, margin: "8px 0" };

const CarteSolde = defineComponent({
  name: "CarteSolde",
  description: "Affiche le solde d'un compte.",
  props: z.object({
    compte: z.string().describe("Nom du compte"),
    solde: z.number().describe("Solde en euros"),
  }),
  component: ({ props }) => (
    <div style={carte}>
      <div>{props.compte}</div>
      <strong style={{ fontSize: 22 }}>{props.solde.toLocaleString("fr-FR")} €</strong>
    </div>
  ),
});

const Transaction = defineComponent({
  name: "Transaction",
  description: "Une ligne de transaction : libellé et montant en euros.",
  props: z.object({ libelle: z.string(), montant: z.number() }),
  component: ({ props }) => (
    <li style={{ display: "flex", justifyContent: "space-between" }}>
      <span>{props.libelle}</span>
      <span>{props.montant.toLocaleString("fr-FR")} €</span>
    </li>
  ),
});

const ListeTransactions = defineComponent({
  name: "ListeTransactions",
  description: "Liste de transactions avec un titre.",
  props: z.object({ titre: z.string(), transactions: z.array(Transaction.ref) }),
  component: ({ props, renderNode }) => (
    <div style={carte}>
      <strong>{props.titre}</strong>
      <ul style={{ listStyle: "none", padding: 0 }}>{renderNode(props.transactions)}</ul>
    </div>
  ),
});

const ConfirmationVirement = defineComponent({
  name: "ConfirmationVirement",
  description:
    "Récapitulatif d'un virement à faire valider par l'utilisateur. Ne jamais considérer le virement comme effectué.",
  props: z.object({ montant: z.number(), beneficiaire: z.string() }),
  component: ({ props }) => {
    const declencher = useTriggerAction();
    return (
      <div style={carte}>
        Virement de <strong>{props.montant} €</strong> vers <strong>{props.beneficiaire}</strong>
        <div style={{ marginTop: 8, display: "flex", gap: 8 }}>
          <button onClick={() => declencher(`Je confirme le virement de ${props.montant} € vers ${props.beneficiaire}`)}>
            Confirmer
          </button>
          <button onClick={() => declencher("J'annule le virement")}>Annuler</button>
        </div>
      </div>
    );
  },
});

const Texte = defineComponent({
  name: "Texte",
  description: "Paragraphe de texte.",
  props: z.object({ texte: z.string() }),
  component: ({ props }) => <p>{props.texte}</p>,
});

const Pile = defineComponent({
  name: "Pile",
  description: "Conteneur racine : empile verticalement ses éléments.",
  props: z.object({
    elements: z.array(
      z.union([CarteSolde.ref, ListeTransactions.ref, ConfirmationVirement.ref, Texte.ref]),
    ),
  }),
  component: ({ props, renderNode }) => <div>{renderNode(props.elements)}</div>,
});

export const bibliotheque = createLibrary({
  root: "Pile",
  components: [Pile, CarteSolde, ListeTransactions, Transaction, ConfirmationVirement, Texte],
});
