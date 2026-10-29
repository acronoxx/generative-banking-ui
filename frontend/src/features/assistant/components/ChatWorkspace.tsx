import { useRef } from 'react'
import { useAssistantDemo } from '../hooks/useAssistantDemo'
import { AgentToolbar } from './AgentToolbar'
import { AgentWelcome } from './AgentWelcome'
import { ConversationSidebar } from './ConversationSidebar'
import { MessageComposer } from './MessageComposer'
import { MessageList } from './MessageList'
import { QuickActions } from './QuickActions'
import styles from './ChatWorkspace.module.css'

type ChatWorkspaceProps = { onGuide: () => void }

export function ChatWorkspace({ onGuide }: ChatWorkspaceProps) {
  const assistant = useAssistantDemo()
  const inputRef = useRef<HTMLTextAreaElement>(null)

  function newConversation() {
    assistant.newConversation()
    inputRef.current?.focus()
  }

  function choosePrompt(prompt: string) {
    assistant.setDraft(prompt)
    inputRef.current?.focus()
  }

  function sendMessage() {
    if (assistant.sendMessage()) inputRef.current?.focus()
  }

  return (
    <section className={styles.workspace} aria-label="Votre assistant bancaire">
      <ConversationSidebar
        conversations={assistant.conversations}
        activeId={assistant.activeConversation.id}
        onSelect={assistant.selectConversation}
        onNew={newConversation}
        onGuide={onGuide}
      />
      <div className={styles.assistant}>
        <AgentToolbar />
        <div className={styles.content}>
          <AgentWelcome />
          {assistant.activeConversation.messages.length === 0 ? (
            <QuickActions onChoose={choosePrompt} />
          ) : (
            <MessageList messages={assistant.activeConversation.messages} />
          )}
          <MessageComposer
            draft={assistant.draft}
            attachment={assistant.attachment}
            inputRef={inputRef}
            onDraftChange={assistant.setDraft}
            onAttachmentChange={assistant.setAttachment}
            onSend={sendMessage}
          />
          <p id="assistant-disclaimer" className={styles.disclaimer}>
            Vérifiez les informations sensibles avant validation. Les montants et les coordonnées sont des exemples.
          </p>
        </div>
      </div>
    </section>
  )
}
