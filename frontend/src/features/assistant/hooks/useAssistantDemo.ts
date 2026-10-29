import { useState } from 'react'
import { appendDemoExchange, createConversation, createDemoExchange } from '../conversation'
import { initialConversations } from '../data/assistant.data'
import type { Conversation } from '../types'

export function useAssistantDemo() {
  const [conversations, setConversations] = useState<Conversation[]>(initialConversations)
  const [activeId, setActiveId] = useState(initialConversations[0].id)
  const [draft, setDraft] = useState('')
  const [attachment, setAttachment] = useState<File | null>(null)
  const activeConversation = conversations.find(({ id }) => id === activeId) ?? conversations[0]

  function selectConversation(id: string) {
    if (!conversations.some((conversation) => conversation.id === id)) return
    setActiveId(id)
    resetComposer()
  }

  function newConversation() {
    const conversation = createConversation()
    setConversations((current) => [conversation, ...current])
    setActiveId(conversation.id)
    resetComposer()
  }

  function sendMessage() {
    const text = draft.trim()
    if (!text && !attachment) return false

    const exchange = createDemoExchange(text, attachment?.name)
    setConversations((current) => current.map((conversation) =>
      conversation.id === activeConversation.id ? appendDemoExchange(conversation, exchange) : conversation,
    ))
    resetComposer()
    return true
  }

  function resetComposer() {
    setDraft('')
    setAttachment(null)
  }

  return {
    conversations,
    activeConversation,
    draft,
    attachment,
    setDraft,
    setAttachment,
    selectConversation,
    newConversation,
    sendMessage,
  }
}
