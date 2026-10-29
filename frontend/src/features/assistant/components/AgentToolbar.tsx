import { Icon } from '../../../components/ui/Icon'
import styles from './AgentToolbar.module.css'

export function AgentToolbar() {
  return (
    <div className={styles.toolbar}>
      <div className={styles.title}><Icon name="agent" size={18} /><span>Mon agent bancaire</span></div>
      <div className={styles.selector}>
        <label className="sr-only" htmlFor="assistant-type">Choisir un assistant</label>
        <select id="assistant-type" defaultValue="banking"><option value="banking">Assistant bancaire</option></select>
        <Icon name="chevron-down" size={16} />
      </div>
    </div>
  )
}
