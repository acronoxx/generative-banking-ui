import { useState } from 'react'
import { Icon } from '../../../components/ui/Icon'
import type { Conversation } from '../types'
import styles from './ConversationSidebar.module.css'

type ConversationSidebarProps = {
  conversations: readonly Conversation[]
  activeId: string
  onSelect: (id: string) => void
  onNew: () => void
  onGuide: () => void
}

export function ConversationSidebar({
  conversations,
  activeId,
  onSelect,
  onNew,
  onGuide,
}: ConversationSidebarProps) {
  const [searchOpen, setSearchOpen] = useState(false)
  const [query, setQuery] = useState('')
  const filteredConversations = conversations.filter(({ title }) =>
    title.toLocaleLowerCase('fr').includes(query.toLocaleLowerCase('fr')),
  )

  return (
    <aside className={styles.sidebar} aria-label="Historique des conversations">
      <button type="button" className={styles.newConversation} onClick={onNew}>
        <Icon name="plus" size={22} />
        Nouvelle conversation
      </button>
      <div className={styles.history}>
        <div className={styles.heading}>
          <h2>Conversations récentes</h2>
          <button
            type="button"
            className="icon-button"
            aria-label={searchOpen ? 'Fermer la recherche' : 'Rechercher une conversation'}
            aria-expanded={searchOpen}
            aria-controls="conversation-search"
            onClick={() => {
              setSearchOpen((open) => !open)
              setQuery('')
            }}
          >
            <Icon name={searchOpen ? 'close' : 'search'} size={17} />
          </button>
        </div>
        {searchOpen && (
          <input
            id="conversation-search"
            className={styles.search}
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Rechercher…"
            aria-label="Rechercher une conversation"
            autoFocus
          />
        )}
        <ul className={styles.list}>
          {filteredConversations.map((conversation, index) => (
            <li key={conversation.id}>
              {index === 1 && <p className={styles.date}>Aujourd’hui</p>}
              <button
                type="button"
                className={`${styles.conversation} ${conversation.id === activeId ? styles.selected : ''}`}
                onClick={() => onSelect(conversation.id)}
                aria-current={conversation.id === activeId ? 'true' : undefined}
                title={conversation.title}
              >
                <Icon name={conversation.icon} size={16} />
                <span>{conversation.title}</span>
              </button>
            </li>
          ))}
        </ul>
        {filteredConversations.length === 0 && <p className={styles.empty}>Aucune conversation trouvée.</p>}
      </div>
      <div className={styles.tip}>
        <div className={styles.tipTitle}>
          <Icon name="lightbulb" size={18} />
          <strong>Un petit conseil</strong>
        </div>
        <p>Précisez votre contexte, votre objectif et le format attendu.</p>
        <button type="button" className={`text-button ${styles.guide}`} onClick={onGuide}>
          Voir le guide des prompts
          <Icon name="arrow-right" size={17} />
        </button>
      </div>
    </aside>
  )
}
