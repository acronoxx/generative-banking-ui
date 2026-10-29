import { Icon } from '../../../components/ui/Icon'
import styles from './AgentWelcome.module.css'

export function AgentWelcome() {
  return (
    <div className={styles.welcome}>
      <div className={styles.avatar}><Icon name="agent" size={24} /></div>
      <div className={styles.copy}>
        <p className={styles.name}>SoprIA_Agent</p>
        <h2>Comment puis-je vous aider pour vos comptes aujourd’hui ?</h2>
        <p className={styles.description}>Bonjour ! Je suis votre assistant bancaire. Dites-moi ce que vous souhaitez faire : consulter un compte, faire un virement, demander un relevé ou autre chose.</p>
      </div>
    </div>
  )
}
