import { useEffect, useRef } from 'react'
import { informationContent } from '../data/information'
import type { InformationTopic } from '../data/information'
import { Icon } from './ui/Icon'
import styles from './InformationDialog.module.css'

type InformationDialogProps = {
  topic: InformationTopic | null
  onClose: () => void
}

export function InformationDialog({ topic, onClose }: InformationDialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null)

  useEffect(() => {
    const dialog = dialogRef.current
    if (topic && dialog && !dialog.open) dialog.showModal()
    if (!topic && dialog?.open) dialog.close()
  }, [topic])

  return (
    <dialog ref={dialogRef} className={styles.dialog} onCancel={onClose}
      onClick={(event) => {
        const rect = event.currentTarget.getBoundingClientRect()
        if (event.target === event.currentTarget && (
          event.clientX < rect.left || event.clientX > rect.right ||
          event.clientY < rect.top || event.clientY > rect.bottom
        )) onClose()
      }} aria-labelledby="information-title">
      {topic && <>
        <div className={styles.heading}>
          <h2 id="information-title">{informationContent[topic].title}</h2>
          <button type="button" className="icon-button" onClick={onClose} aria-label="Fermer"><Icon name="close" /></button>
        </div>
        <div className={styles.content}>
          {informationContent[topic].paragraphs.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}
        </div>
        <button type="button" className={styles.done} onClick={onClose}>Compris</button>
      </>}
    </dialog>
  )
}
