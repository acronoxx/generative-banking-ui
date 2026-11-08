import { useEffect, useState } from 'react'
import { Icon } from '../components/ui/Icon'
import type { InformationTopic } from '../data/information'
import { BankingPreferences } from '../features/profile/components/BankingPreferences'
import { EditProfileDialog } from '../features/profile/components/EditProfileDialog'
import { PersonalInformation } from '../features/profile/components/PersonalInformation'
import { ProfileOverview } from '../features/profile/components/ProfileOverview'
import { ProfileSidebar } from '../features/profile/components/ProfileSidebar'
import { SecuritySettings } from '../features/profile/components/SecuritySettings'
import { useProfile } from '../features/profile/hooks/useProfile'
import ui from '../features/profile/components/ProfileSections.module.css'
import styles from './ProfilePage.module.css'

type Props = { hidden: boolean; section: string; onInformation: (topic: InformationTopic) => void }

export function ProfilePage({ hidden, section, onInformation }: Props) {
  const { state, retry, updateContact } = useProfile()
  const [editing, setEditing] = useState(false)
  const [notice, setNotice] = useState('')
  const unavailable = () => onInformation('profile-service')
  const profile = state.status === 'ready' ? state.profile : null

  useEffect(() => {
    if (hidden || !section || state.status !== 'ready') return
    const target = document.getElementById(section)
    target?.focus({ preventScroll: true })
    target?.scrollIntoView({ block: 'start' })
  }, [hidden, section, state.status])

  return (
    <main hidden={hidden} className={`page-container ${styles.main}`} aria-labelledby="profile-title">
      <div className={styles.pageHeading}>
        <nav className={styles.breadcrumb} aria-label="Fil d’Ariane"><a href="#/accueil">Espace Client</a><span aria-hidden="true">/</span><span aria-current="page">Profil & Paramètres</span></nav>
        <div className={styles.headingRow}>
          <div>
            <div className={styles.titleRow}><h1 id="profile-title" tabIndex={-1}>Mon profil</h1>{profile?.certified && <span className={ui.badge}>● Compte certifié DSP2 · Démo</span>}</div>
            <p>Consultez et gérez vos données personnelles, vos dispositifs de sécurité et vos préférences bancaires.</p>
          </div>
          <div className={ui.buttonRow}>
            <button type="button" className={ui.button} onClick={unavailable}><Icon name="download" size={16} />Télécharger mon RIB</button>
            <button type="button" className={ui.primaryButton} onClick={() => setEditing(true)} disabled={!profile}><Icon name="edit" size={16} />Modifier le profil</button>
          </div>
        </div>
      </div>
      {state.status === 'loading' && <p className={styles.state} role="status">Chargement du profil…</p>}
      {state.status === 'error' && <div className={styles.state} role="alert"><p>Le profil n’a pas pu être chargé.</p><button type="button" className={ui.button} onClick={retry}>Réessayer</button></div>}
      {state.status === 'ready' && !profile && <div className={styles.state}><p>Aucun profil disponible.</p><button type="button" className={ui.button} onClick={retry}>Actualiser</button></div>}
      {profile && <div className={styles.layout}>
        <ProfileSidebar advisor={profile.advisor} section={section || 'coordonnees'} onUnavailable={unavailable} />
        <div className={styles.content}>
          <ProfileOverview profile={profile} onUnavailable={unavailable} />
          <p className={styles.demoNote}>Données fictives de démonstration. Aucun compte bancaire réel n’est connecté. Les modifications sont conservées en mémoire jusqu’au rechargement.</p>
          <p className={styles.notice} role="status">{notice}</p>
          <PersonalInformation personal={profile.personal} onEdit={() => setEditing(true)} onUnavailable={unavailable} />
          <BankingPreferences card={profile.card} limit={profile.paymentLimit} preferences={profile.preferences} onUnavailable={unavailable} />
          <SecuritySettings security={profile.security} onUnavailable={unavailable} />
          <section className={styles.support} aria-labelledby="profile-support-title">
            <div><h2 id="profile-support-title">{profile.support.name}</h2><p>{profile.support.hours}</p></div>
            <div className={ui.buttonRow}>
              <button type="button" className={ui.button} onClick={() => onInformation('help')}>Aide en ligne & FAQ</button>
              <button type="button" className={ui.primaryButton} onClick={unavailable}>Contacter mon conseiller</button>
            </div>
          </section>
          <p className={styles.regulatory}>Les services bancaires soumis à la réglementation européenne DSP2 peuvent nécessiter une authentification forte pour modifier des coordonnées sensibles. Cette démonstration ne réalise aucune vérification réglementaire.</p>
        </div>
      </div>}
      {editing && profile && !hidden && <EditProfileDialog contact={profile.personal} onClose={() => setEditing(false)} onSave={(contact) => {
        updateContact(contact)
        setEditing(false)
        setNotice('Coordonnées de démonstration mises à jour localement. Aucune modification bancaire effectuée.')
      }} />}
    </main>
  )
}
