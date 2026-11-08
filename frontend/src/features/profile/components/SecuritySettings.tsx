import { Icon } from '../../../components/ui/Icon'
import type { IconName } from '../../../components/ui/Icon'
import type { SecuritySettings as SecurityData } from '../types'
import { formatDate } from '../format'
import styles from './ProfileSections.module.css'

export function SecuritySettings({ security, onUnavailable }: { security: SecurityData; onUnavailable: () => void }) {
  const items: { title: string; icon: IconName; description: string; detail: string; action: string }[] = [
    { title: 'Clé Digitale (DSP2)', icon: 'phone', description: `Enregistrée sur ${security.deviceName}.`, detail: `Dernière validation de démonstration : ${formatDate(security.lastValidation)}.`, action: 'Gérer mes appareils' },
    { title: 'Code secret de connexion', icon: 'password', description: 'Code à 6 chiffres pour l’accès web.', detail: `Dernière modification (démo) : ${formatDate(security.codeUpdatedAt)}.`, action: 'Modifier le code' },
    { title: 'Contact de confiance', icon: 'shield', description: 'Mandataire ou tiers autorisé en cas d’urgence ou d’indisponibilité.', detail: security.trustedContactName ?? 'Aucun mandataire désigné.', action: 'Désigner un contact' },
  ]
  return (
    <section id="securite" tabIndex={-1} className={styles.panel} aria-labelledby="security-title">
      <div className={styles.sectionHeading}><h2 id="security-title">Dispositifs de sécurité & Accès</h2><p>Protection de votre espace bancaire et validation des opérations sensibles.</p></div>
      <div className={styles.securityGrid}>
        {items.map((item) => <div className={styles.innerCard} key={item.title}>
          <h3 className={styles.iconTitle}><Icon name={item.icon} size={21} />{item.title}</h3>
          <p>{item.description}</p><p className={styles.muted}>{item.detail}</p>
          <div className={styles.cardActions}><button type="button" className="text-button" onClick={onUnavailable}>{item.action}</button></div>
        </div>)}
      </div>
    </section>
  )
}
