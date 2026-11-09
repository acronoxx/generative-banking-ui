// Interface de conversation construite avec les primitives d'assistant-ui,
// branchée sur l'agent de l'essai genui-ai-sdk (même serveur, port 4100).
// Les primitives n'imposent aucun style : l'application fournit le sien.
import {
  AssistantRuntimeProvider,
  ComposerPrimitive,
  MessagePrimitive,
  ThreadPrimitive,
  type ToolCallMessagePartComponent,
} from '@assistant-ui/react'
import { useChatRuntime } from '@assistant-ui/ai-sdk'
import { lastAssistantMessageIsCompleteWithApprovalResponses } from 'ai'

const euros = (montant: number) => `${montant.toLocaleString('fr-FR')} €`

// Composants de l'application associés aux outils de l'agent
const Solde: ToolCallMessagePartComponent<{ account: string }, { compte: string; solde: number }> = ({ result }) =>
  result ? (
    <div className="carte">
      <span>Compte {result.compte}</span>
      <strong>{euros(result.solde)}</strong>
    </div>
  ) : (
    <p className="attente">Consultation du solde…</p>
  )

const Transactions: ToolCallMessagePartComponent<{ min_amount: number }, { libelle: string; montant: number }[]> = ({ args, result }) =>
  result ? (
    <div className="carte">
      <span>Transactions supérieures à {euros(args.min_amount)}</span>
      <ul>
        {result.map((t) => (
          <li key={t.libelle}>
            {t.libelle} <strong>{euros(t.montant)}</strong>
          </li>
        ))}
      </ul>
    </div>
  ) : (
    <p className="attente">Recherche des transactions…</p>
  )

// Validation humaine : l'agent attend la réponse à la demande d'approbation
const Virement: ToolCallMessagePartComponent<{ amount: number; beneficiary: string }> = ({ args, result, approval, respondToApproval }) => {
  if (approval && approval.approved === undefined)
    return (
      <div className="carte confirmation">
        <span>Virement de {euros(args.amount)} vers {args.beneficiary}</span>
        <div>
          <button onClick={() => respondToApproval({ approved: true })}>Confirmer</button>
          <button onClick={() => respondToApproval({ approved: false })}>Refuser</button>
        </div>
      </div>
    )
  if (result) return <div className="carte">Virement simulé de {euros(args.amount)} vers {args.beneficiary}</div>
  return <p className="attente">Virement {approval?.approved === false ? 'refusé' : 'en cours'}.</p>
}

const OUTILS = { by_name: { get_balance: Solde, get_transactions: Transactions, prepare_transfer: Virement } }

export default function App() {
  // Envoie la conversation à /api/chat (relayé vers le serveur de l'agent par Vite) ;
  // après une approbation ou un refus, la conversation repart vers l'agent
  const runtime = useChatRuntime({ sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithApprovalResponses })

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <main className="page">
        <h1>Assistant bancaire</h1>
        <ThreadPrimitive.Root>
          <ThreadPrimitive.Viewport>
            <ThreadPrimitive.Messages>
              {({ message }) => (
                <MessagePrimitive.Root className={`message ${message.role}`}>
                  <MessagePrimitive.Parts components={{ tools: OUTILS }} />
                </MessagePrimitive.Root>
              )}
            </ThreadPrimitive.Messages>
          </ThreadPrimitive.Viewport>
          <ComposerPrimitive.Root>
            <ComposerPrimitive.Input placeholder="Votre demande…" />
            <ComposerPrimitive.Send>Envoyer</ComposerPrimitive.Send>
          </ComposerPrimitive.Root>
        </ThreadPrimitive.Root>
      </main>
    </AssistantRuntimeProvider>
  )
}
