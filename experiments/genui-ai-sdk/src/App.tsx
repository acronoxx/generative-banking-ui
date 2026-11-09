// Interface générative « statique » avec l'AI SDK de Vercel : chaque outil de
// l'agent est associé à un composant React écrit à l'avance.
import { useState } from 'react'
import { useChat } from '@ai-sdk/react'
import { DefaultChatTransport, lastAssistantMessageIsCompleteWithApprovalResponses } from 'ai'
import type { MessageBanque } from '../agent.ts'

const euros = (montant: number) => `${montant.toLocaleString('fr-FR')} €`

export default function App() {
  const [saisie, setSaisie] = useState('')
  const { messages, sendMessage, status, addToolApprovalResponse } = useChat<MessageBanque>({
    transport: new DefaultChatTransport({ api: '/api/chat' }),
    // Après une approbation ou un refus, la conversation repart vers l'agent
    sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithApprovalResponses,
  })

  return (
    <main className="page">
      <h1>Assistant bancaire</h1>

      {messages.map((message) => (
        <div key={message.id} className={`message ${message.role}`}>
          {message.parts.map((part, i) => {
            switch (part.type) {
              case 'text':
                return <p key={i}>{part.text}</p>

              case 'tool-get_balance':
                if (part.state !== 'output-available') return <p key={i} className="attente">Consultation du solde…</p>
                return (
                  <div key={i} className="carte">
                    <span>Compte {part.output.compte}</span>
                    <strong>{euros(part.output.solde)}</strong>
                  </div>
                )

              case 'tool-get_transactions':
                if (part.state !== 'output-available') return <p key={i} className="attente">Recherche des transactions…</p>
                return (
                  <div key={i} className="carte">
                    <span>Transactions supérieures à {euros(part.input.min_amount)}</span>
                    <ul>
                      {part.output.map((t) => (
                        <li key={t.libelle}>
                          {t.libelle} <strong>{euros(t.montant)}</strong>
                        </li>
                      ))}
                    </ul>
                  </div>
                )

              case 'tool-prepare_transfer':
                // Validation humaine : l'outil ne s'exécute qu'après accord de l'utilisateur
                if (part.state === 'approval-requested')
                  return (
                    <div key={i} className="carte confirmation">
                      <span>Virement de {euros(part.input.amount)} vers {part.input.beneficiary}</span>
                      <div>
                        <button onClick={() => addToolApprovalResponse({ id: part.approval.id, approved: true })}>Confirmer</button>
                        <button onClick={() => addToolApprovalResponse({ id: part.approval.id, approved: false })}>Refuser</button>
                      </div>
                    </div>
                  )
                if (part.state === 'output-available')
                  return <div key={i} className="carte">Virement {part.output.statut} de {euros(part.output.amount)} vers {part.output.beneficiary}</div>
                if (part.state === 'output-denied') return <p key={i} className="attente">Virement refusé.</p>
                return null

              default:
                return null
            }
          })}
        </div>
      ))}

      <form
        onSubmit={(e) => {
          e.preventDefault()
          if (!saisie.trim()) return
          sendMessage({ text: saisie })
          setSaisie('')
        }}
      >
        <input value={saisie} onChange={(e) => setSaisie(e.target.value)} placeholder="Votre demande…" disabled={status !== 'ready'} />
        <button type="submit" disabled={status !== 'ready'}>Envoyer</button>
      </form>
    </main>
  )
}
