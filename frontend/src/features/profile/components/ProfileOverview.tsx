import { Icon } from '../../../components/ui/Icon'
import type { UserProfile } from '../types'
import styles from './ProfileSections.module.css'

export function ProfileOverview({ profile, onUnavailable }: { profile: UserProfile; onUnavailable: () => void }) {
  const { personal, accounts, card } = profile
  return (
    <section className={styles.panel} aria-labelledby="overview-title">
      <div className={styles.overview}>
        <div className={styles.identity}>
          <div className={styles.avatar} aria-hidden="true">
            {personal.firstName.charAt(0)}{personal.lastName.charAt(0)}
            {personal.identityVerified && <span><Icon name="check" size={13} /></span>}
          </div>
          <div>
            <h2 id="overview-title">{personal.firstName} {personal.lastName}</h2>
            <div className={styles.metadata}>
              <span>Identifiant client : <strong className={styles.mono}>{profile.clientReference}</strong></span>
              <span>Agence : <strong>{profile.agency}</strong></span>
            </div>
          </div>
        </div>
        <div className={styles.overviewActions}>
          <button type="button" className={styles.softButton} onClick={onUnavailable}><Icon name="camera" size={16} />Changer la photo</button>
          <button type="button" className={styles.button} onClick={onUnavailable}><Icon name="file" size={16} />Attestation bancaire</button>
        </div>
      </div>
      <div className={styles.accountGrid}>
        {accounts.map((account) => <div className={styles.summary} key={account.id}>
          <h3 className={styles.eyebrow}>{account.kind === 'current' ? 'Compte principal' : 'Épargne liée'}</h3>
          <strong>{account.name}</strong>
          <p className={account.maskedNumber ? styles.mono : undefined}>{account.maskedNumber ?? account.description}</p>
        </div>)}
        {accounts.length === 0 && <p className={styles.muted}>Aucun compte associé.</p>}
        <div className={styles.summary}>
          <h3 className={styles.eyebrow}>Moyen de paiement</h3>
          {card ? <>
            <div className={styles.between}><strong>{card.name}</strong><span className={styles.badge}>{card.active ? 'Active' : 'Inactive'}</span></div>
            <p className={styles.mono}>N° **** {card.lastFour} · {card.expiresAt}</p>
          </> : <p>Aucune carte associée.</p>}
        </div>
      </div>
    </section>
  )
}
