import { Icon } from '../../../components/ui/Icon'
import type { IconName } from '../../../components/ui/Icon'
import type { BankingAdvisor } from '../types'
import styles from './ProfileSections.module.css'

const links: { id: string; label: string; icon: IconName }[] = [
  { id: 'coordonnees', label: 'État civil & Coordonnées', icon: 'user' },
  { id: 'comptes', label: 'Comptes & Plafonds', icon: 'bank' },
  { id: 'securite', label: 'Sécurité & Clé Digitale', icon: 'shield' },
  { id: 'documents', label: 'Relevés & e-Documents', icon: 'file' },
  { id: 'alertes', label: 'Alertes & Notifications', icon: 'bell' },
]

type Props = { advisor: BankingAdvisor | null; section: string; onUnavailable: () => void }

export function ProfileSidebar({ advisor, section, onUnavailable }: Props) {
  return (
    <aside className={styles.sidebar} aria-label="Navigation du profil et conseiller">
      <nav className={`${styles.panel} ${styles.navigation}`} aria-label="Rubriques du profil">
        <h2 className={styles.eyebrow}>Navigation</h2>
        {links.map((link) => link.id === 'documents' || link.id === 'alertes' ? (
          <button type="button" key={link.id} onClick={onUnavailable}><Icon name={link.icon} size={17} />{link.label}</button>
        ) : (
          <a key={link.id} href={`#/profil/${link.id}`} className={section === link.id ? styles.selected : undefined}
            aria-current={section === link.id ? 'location' : undefined}>
            <Icon name={link.icon} size={17} />{link.label}
            {link.id === 'securite' && <span className={styles.badge}>Démo</span>}
          </a>
        ))}
      </nav>
      <section className={styles.panel} aria-labelledby="advisor-title">
        <div className={styles.between}>
          <h2 id="advisor-title" className={styles.eyebrow}>Votre conseiller privé</h2>
          {advisor && <span className={styles.status}>{advisor.available ? '● Disponible' : 'Indisponible'}</span>}
        </div>
        {advisor ? <>
          <div className={styles.advisor}>
            <span className={styles.advisorAvatar} aria-hidden="true">{advisor.initials}</span>
            <div><h3>{advisor.name}</h3><p>{advisor.role}</p><p>{advisor.agency}</p></div>
          </div>
          <div className={styles.buttonRow}>
            <button type="button" className={styles.softButton} onClick={onUnavailable}><Icon name="calendar" size={16} />Rendez-vous</button>
            <button type="button" className={styles.button} onClick={onUnavailable}><Icon name="mail" size={16} />Message</button>
          </div>
        </> : <p className={styles.muted}>Aucun conseiller affecté à ce profil.</p>}
      </section>
      <div className={styles.securityNote}>
        <Icon name="shield" size={20} />
        <p><strong>Garantie de sécurité</strong><br />Les services bancaires nécessitent des dispositifs de protection conformes aux exigences ACPR & DSP2. Aucun service bancaire n’est connecté ici.</p>
      </div>
    </aside>
  )
}
