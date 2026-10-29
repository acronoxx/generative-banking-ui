import { useEffect, useRef } from 'react'
import type { RefObject } from 'react'
import { Icon } from '../../../components/ui/Icon'
import styles from './MessageComposer.module.css'

type MessageComposerProps = {
  draft: string
  attachment: File | null
  inputRef: RefObject<HTMLTextAreaElement | null>
  onDraftChange: (value: string) => void
  onAttachmentChange: (file: File | null) => void
  onSend: () => void
}

export function MessageComposer({
  draft,
  attachment,
  inputRef,
  onDraftChange,
  onAttachmentChange,
  onSend,
}: MessageComposerProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (!attachment && fileInputRef.current) fileInputRef.current.value = ''
  }, [attachment])

  return (
    <form
      className={styles.composer}
      onSubmit={(event) => {
        event.preventDefault()
        onSend()
      }}
    >
      <label htmlFor="assistant-message" className="sr-only">
        Votre demande à l’assistant bancaire
      </label>
      <textarea
        id="assistant-message"
        ref={inputRef}
        value={draft}
        rows={2}
        onChange={(event) => onDraftChange(event.target.value)}
        placeholder="Dites par exemple : « Je veux faire un virement à … »…"
        aria-describedby="assistant-disclaimer"
        onKeyDown={(event) => {
          if (event.key === 'Enter' && !event.shiftKey && !event.nativeEvent.isComposing) {
            event.preventDefault()
            onSend()
          }
        }}
      />
      {attachment && (
        <div className={styles.attachment}>
          <Icon name="file" size={15} />
          <span>{attachment.name}</span>
          <button
            type="button"
            className="icon-button"
            onClick={() => onAttachmentChange(null)}
            aria-label="Retirer le fichier joint"
          >
            <Icon name="close" size={14} />
          </button>
        </div>
      )}
      <div className={styles.actions}>
        <input
          className="sr-only"
          ref={fileInputRef}
          type="file"
          tabIndex={-1}
          aria-label="Sélectionner un fichier à joindre"
          onChange={(event) => onAttachmentChange(event.target.files?.[0] ?? null)}
        />
        <button type="button" className={styles.attach} onClick={() => fileInputRef.current?.click()}>
          <Icon name="paperclip" size={20} />
          Joindre un fichier
        </button>
        <button type="submit" className={styles.send} disabled={!draft.trim() && !attachment}>
          Envoyer
          <Icon name="arrow-up" size={17} />
        </button>
      </div>
    </form>
  )
}
