import type { PersonalInformation as PersonalInformationData } from '../types'
import { formatDate } from '../format'
import styles from './ProfileSections.module.css'

type Props = { personal: PersonalInformationData; onEdit: () => void; onUnavailable: () => void }

export function PersonalInformation({ personal, onEdit, onUnavailable }: Props) {
  const rows = [
    { label: 'Nom & Prénoms légaux', value: personal.legalName, badge: personal.identityVerified ? 'Vérifié sur CNI' : 'À vérifier', action: 'Justificatif', onClick: onUnavailable },
    { label: 'Date et lieu de naissance', value: `${formatDate(personal.birthDate, true)} à ${personal.birthPlace}` },
    { label: 'Adresse email de contact', value: personal.email, badge: personal.emailVerified ? 'Vérifiée' : 'Non vérifiée', action: 'Modifier', onClick: onEdit },
    { label: 'Numéro de mobile sécurisé', value: personal.phone, badge: personal.phoneVerified ? 'Lié Clé Digitale' : 'Non vérifié', action: 'Modifier', onClick: onEdit },
    { label: 'Adresse fiscale et postale', value: personal.address, action: 'Mettre à jour', onClick: onEdit },
  ]
  return (
    <section id="coordonnees" tabIndex={-1} className={`${styles.panel} ${styles.personal}`} aria-labelledby="personal-title">
      <div className={`${styles.sectionHeading} ${styles.between}`}>
        <div><h2 id="personal-title">Coordonnées & État civil</h2><p>Données personnelles et informations de vérification du profil de démonstration.</p></div>
        <span className={styles.muted}>Dernière mise à jour : {formatDate(personal.updatedAt)}</span>
      </div>
      <dl className={styles.details}>
        {rows.map((row) => <div className={styles.detailRow} key={row.label}>
          <dt>{row.label}</dt>
          <dd><span>{row.value}</span>{row.badge && <span className={styles.verification}>{row.badge}</span>}</dd>
          <dd className={styles.detailAction}>{row.action ? <button type="button" className="text-button" aria-label={`${row.action} — ${row.label}`} onClick={row.onClick}>{row.action}</button> : <span className={styles.muted}>Conforme (démo)</span>}</dd>
        </div>)}
      </dl>
    </section>
  )
}
