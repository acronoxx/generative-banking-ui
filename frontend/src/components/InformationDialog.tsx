import { informationContent } from '../data/information'
import type { InformationTopic } from '../data/information'
import { Dialog } from './ui/Dialog'
import styles from './InformationDialog.module.css'

type InformationDialogProps = {
  topic: InformationTopic | null
  onClose: () => void
}

export function InformationDialog({ topic, onClose }: InformationDialogProps) {
  return (
    <Dialog open={topic !== null} title={topic ? informationContent[topic].title : ''} onClose={onClose}>
      {topic && <>
        <div className={styles.content}>
          {informationContent[topic].paragraphs.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}
        </div>
        <button type="button" className={styles.done} onClick={onClose}>Compris</button>
      </>}
    </Dialog>
  )
}
