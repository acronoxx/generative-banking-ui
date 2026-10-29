import type { InformationTopic } from '../../data/information'
import styles from './Footer.module.css'

type FooterProps = { onInformation: (topic: InformationTopic) => void }

export function Footer({ onInformation }: FooterProps) {
  return (
    <footer className={styles.footer}>
      <div className={`page-container ${styles.inner}`}>
        <div className={styles.copyright}><strong>SoprIA</strong><span className={styles.divider} /><span>© 2026 Sopra Steria</span></div>
        <nav className={styles.links} aria-label="Informations légales et support">
          <button className="text-button" onClick={() => onInformation('terms')}>Conditions d’utilisation</button>
          <button className="text-button" onClick={() => onInformation('privacy')}>Confidentialité</button>
          <button className="text-button" onClick={() => onInformation('support')}>Contacter le support</button>
        </nav>
      </div>
    </footer>
  )
}
