import type { Conversation, Message } from './types'

export function createConversation(): Conversation {
  return {
    id: crypto.randomUUID(),
    title: 'Nouvelle conversation',
    icon: 'bank',
    messages: [],
  }
}

// Demo behavior stays independent of React and never reads or uploads file contents.
export function createDemoExchange(text: string, attachmentName?: string): readonly [Message, Message] {
  return [
    { id: crypto.randomUUID(), role: 'user', text, attachmentName },
    {
      id: crypto.randomUUID(),
      role: 'assistant',
      text: attachmentName !== undefined
        ? 'Votre demande et le nom du fichier ont été ajoutés à cette conversation de démonstration. Le fichier n’a pas été envoyé. Aucune opération bancaire n’a été effectuée.'
        : 'Votre demande a été ajoutée à cette conversation de démonstration. Le service bancaire n’est pas connecté : je ne peux pas encore consulter vos comptes ni effectuer d’opération.',
    },
  ]
}

export function appendDemoExchange(
  conversation: Conversation,
  exchange: readonly [Message, Message],
): Conversation {
  const [message] = exchange

  return {
    ...conversation,
    title: conversation.messages.length
      ? conversation.title
      : (message.text || message.attachmentName || conversation.title),
    messages: [...conversation.messages, ...exchange],
  }
}
