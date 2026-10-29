import { Icon } from '../../../components/ui/Icon'
import { quickActions } from '../data/assistant.data'
import styles from './QuickActions.module.css'

type QuickActionsProps = { onChoose: (prompt: string) => void }

export function QuickActions({ onChoose }: QuickActionsProps) {
  return (
    <section className={styles.section} aria-labelledby="quick-actions-title">
      <h3 id="quick-actions-title">Opérations rapides</h3>
      <div className={styles.grid}>
        {quickActions.map((action) => (
          <button type="button" className={styles.card} key={action.id} onClick={() => onChoose(action.prompt)}>
            <Icon name={action.icon} size={24} />
            <span className={styles.copy}>
              <strong>{action.title}</strong>
              <span>{action.description}</span>
            </span>
            <Icon className={styles.arrow} name="arrow-up-right" size={21} />
          </button>
        ))}
      </div>
    </section>
  )
}
