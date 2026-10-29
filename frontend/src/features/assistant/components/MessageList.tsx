import { useEffect, useRef } from 'react'
import { Icon } from '../../../components/ui/Icon'
import type { Message } from '../types'
import styles from './MessageList.module.css'

type MessageListProps = { messages: readonly Message[] }

export function MessageList({ messages }: MessageListProps) {
  const lastMessageRef = useRef<HTMLDivElement>(null)

  useEffect(() => { lastMessageRef.current?.scrollIntoView({ block: 'nearest' }) }, [messages])

  return (
    <div className={styles.messages} role="log" aria-label="Messages de la conversation" aria-live="polite" aria-relevant="additions">
      {messages.map((message, index) => (
        <div key={message.id} className={`${styles.message} ${message.role === 'user' ? styles.user : ''}`}
          ref={index === messages.length - 1 ? lastMessageRef : undefined}>
          <span className={styles.author}>{message.role === 'user' ? 'Vous' : 'SoprIA_Agent'}</span>
          {message.text && <p>{message.text}</p>}
          {message.attachmentName && <span className={styles.file}><Icon name="paperclip" size={16} />{message.attachmentName}</span>}
        </div>
      ))}
    </div>
  )
}
