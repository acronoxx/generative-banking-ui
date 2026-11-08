import type { BankCard, CustomerPreferences, PaymentLimit } from '../types'
import { formatMoney } from '../format'
import styles from './ProfileSections.module.css'

type Props = { card: BankCard | null; limit: PaymentLimit | null; preferences: CustomerPreferences; onUnavailable: () => void }

export function BankingPreferences({ card, limit, preferences, onUnavailable }: Props) {
  const currency = limit?.currency ?? 'EUR'
  return (
    <section id="comptes" tabIndex={-1} className={styles.panel} aria-labelledby="preferences-title">
      <div className={styles.sectionHeading}>
        <h2 id="preferences-title">Préférences bancaires & Moyens de paiement</h2>
        <p>Gérez vos autorisations, plafonds d’opérations et options de cartes.</p>
      </div>
      <div className={styles.preferenceGrid}>
        <div className={styles.innerCard}>
          <div className={styles.between}><h3>Plafond de paiement par carte</h3>{limit && <span className={styles.verification}>{limit.rollingDays} jours glissants</span>}</div>
          {limit ? <>
            <p className={styles.muted}>Plafond total autorisé : <strong>{formatMoney(limit.total, currency)}</strong></p>
            <div className={styles.limitLabels}><span>Utilisé : <strong>{formatMoney(limit.used, currency)}</strong></span><span>Disponible : <strong>{formatMoney(Math.max(0, limit.total - limit.used), currency)}</strong></span></div>
            <progress className={styles.progress} value={Math.max(0, Math.min(limit.used, limit.total))} max={Math.max(1, limit.total)} aria-label="Plafond de paiement utilisé" />
          </> : <p className={styles.muted}>Aucun plafond de paiement disponible.</p>}
          <div className={styles.cardActions}><button type="button" className="text-button" onClick={onUnavailable}>Ajuster le plafond →</button></div>
        </div>
        <div className={styles.innerCard}>
          <div className={styles.between}><h3>Options de la carte {card?.name ?? 'bancaire'}</h3>{card && <span className={styles.mono}>**** {card.lastFour}</span>}</div>
          {card ? <dl className={styles.options}>
            <div><dt>Paiement sans contact :</dt><dd className={styles.status}>{preferences.contactless ? `● Activé (max. ${formatMoney(preferences.contactlessLimit, currency)})` : 'Désactivé'}</dd></div>
            <div><dt>Paiements à l’étranger :</dt><dd className={styles.status}>● {preferences.internationalZone}</dd></div>
            <div><dt>Paiements sur Internet (3D Secure) :</dt><dd>{preferences.onlinePayments ? 'Actif' : 'Inactif'}</dd></div>
          </dl> : <p className={styles.muted}>Aucune carte associée.</p>}
          <div className={`${styles.cardActions} ${styles.between}`}>
            <button type="button" className={`text-button ${styles.danger}`} onClick={onUnavailable}>Opposition temporaire</button>
            <button type="button" className="text-button" onClick={onUnavailable}>Paramètres carte →</button>
          </div>
        </div>
      </div>
    </section>
  )
}
