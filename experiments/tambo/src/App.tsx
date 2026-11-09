// Essai préparé mais NON exécuté : Tambo nécessite une clé de son service
// (VITE_TAMBO_API_KEY dans un fichier .env), ou un serveur Tambo auto-hébergé.
// La boucle de l'agent est assurée par le serveur Tambo, pas par l'application.
import { TamboProvider, defineTool, useTambo, useTamboThreadInput, type TamboComponent } from '@tambo-ai/react'
import { z } from 'zod'

const euros = (montant: number) => `${montant.toLocaleString('fr-FR')} €`

// 1. Composants de l'application, décrits par le schéma de leurs propriétés.
//    Le modèle choisit le composant et en produit les propriétés.
const propsCarteSolde = z.object({ compte: z.string(), solde: z.number() })
function CarteSolde({ compte, solde }: z.infer<typeof propsCarteSolde>) {
  return (
    <div className="carte">
      <span>Compte {compte}</span>
      <strong>{euros(solde)}</strong>
    </div>
  )
}

const propsListeTransactions = z.object({
  titre: z.string(),
  transactions: z.array(z.object({ libelle: z.string(), montant: z.number() })),
})
function ListeTransactions({ titre, transactions }: z.infer<typeof propsListeTransactions>) {
  return (
    <div className="carte">
      <span>{titre}</span>
      <ul>
        {transactions.map((t) => (
          <li key={t.libelle}>
            {t.libelle} <strong>{euros(t.montant)}</strong>
          </li>
        ))}
      </ul>
    </div>
  )
}

const COMPOSANTS: TamboComponent[] = [
  { name: 'CarteSolde', description: "Affiche le solde d'un compte.", component: CarteSolde, propsSchema: propsCarteSolde },
  { name: 'ListeTransactions', description: 'Affiche une liste de transactions.', component: ListeTransactions, propsSchema: propsListeTransactions },
]

// 2. Outils exécutés dans la page, appelés par le serveur Tambo
const TRANSACTIONS = [
  { libelle: 'Loyer', montant: 780 },
  { libelle: 'Garage', montant: 620 },
  { libelle: 'Courses', montant: 95 },
  { libelle: 'Billets de train', montant: 510 },
]

const OUTILS = [
  defineTool({
    name: 'get_balance',
    description: "Renvoie le solde d'un compte ('courant' ou 'livret').",
    tool: async ({ account }) => ({ compte: account, solde: account === 'courant' ? 1250 : 8400 }),
    inputSchema: z.object({ account: z.enum(['courant', 'livret']) }),
    outputSchema: z.object({ compte: z.string(), solde: z.number() }),
  }),
  defineTool({
    name: 'get_transactions',
    description: 'Renvoie les transactions des trois derniers mois supérieures à un montant en euros.',
    tool: async ({ min_amount }) => TRANSACTIONS.filter((t) => t.montant >= min_amount),
    inputSchema: z.object({ min_amount: z.number() }),
    outputSchema: z.array(z.object({ libelle: z.string(), montant: z.number() })),
  }),
]

function Conversation() {
  const { messages, isStreaming } = useTambo()
  const { value, setValue, submit, isPending } = useTamboThreadInput()

  return (
    <main className="page">
      <h1>Assistant bancaire</h1>
      {messages.map((message) => (
        <div key={message.id} className={`message ${message.role}`}>
          {message.content.map((contenu, i) => {
            if (contenu.type === 'text') return <p key={i}>{contenu.text}</p>
            // Le composant choisi par le modèle, déjà rendu avec ses propriétés
            if (contenu.type === 'component') return <div key={i}>{contenu.renderedComponent}</div>
            return null
          })}
        </div>
      ))}
      {isStreaming && <p className="attente">…</p>}
      <form
        onSubmit={(e) => {
          e.preventDefault()
          void submit()
        }}
      >
        <input value={value} onChange={(e) => setValue(e.target.value)} placeholder="Votre demande…" />
        <button type="submit" disabled={isPending}>Envoyer</button>
      </form>
    </main>
  )
}

export default function App() {
  return (
    <TamboProvider apiKey={import.meta.env.VITE_TAMBO_API_KEY} userKey="client-demo" components={COMPOSANTS} tools={OUTILS}>
      <Conversation />
    </TamboProvider>
  )
}
