import { useState } from 'react'
import { Dialog } from '../../../components/ui/Dialog'
import type { ProfileContact } from '../types'
import styles from './ProfileSections.module.css'

type Props = { contact: ProfileContact; onSave: (contact: ProfileContact) => void; onClose: () => void }

export function EditProfileDialog({ contact, onSave, onClose }: Props) {
  const [draft, setDraft] = useState(contact)
  return (
    <Dialog open title="Modifier le profil" onClose={onClose}>
      <form className={styles.editForm} onSubmit={(event) => {
        event.preventDefault()
        onSave({ email: draft.email.trim(), phone: draft.phone.trim(), address: draft.address.trim() })
      }}>
        <p id="edit-demo-note" className={styles.demoNote}>Modification locale des données de démonstration. Aucun changement n’est envoyé à une banque. Les coordonnées modifiées ne sont pas vérifiées.</p>
        <label htmlFor="profile-email">Adresse email de contact</label>
        <input id="profile-email" type="email" required maxLength={254} value={draft.email} onChange={(event) => setDraft({ ...draft, email: event.target.value })} aria-describedby="edit-demo-note" />
        <label htmlFor="profile-phone">Numéro de mobile</label>
        <input id="profile-phone" type="tel" required pattern=".*\S.*" maxLength={40} value={draft.phone} onChange={(event) => setDraft({ ...draft, phone: event.target.value })} />
        <label htmlFor="profile-address">Adresse fiscale et postale</label>
        <textarea id="profile-address" required maxLength={300} rows={3} value={draft.address} onChange={(event) => {
          event.target.setCustomValidity(event.target.value.trim() ? '' : 'Veuillez renseigner une adresse.')
          setDraft({ ...draft, address: event.target.value })
        }} />
        <div className={styles.buttonRow}>
          <button type="button" className={styles.button} onClick={onClose}>Annuler</button>
          <button type="submit" className={styles.primaryButton}>Enregistrer pour la démo</button>
        </div>
      </form>
    </Dialog>
  )
}
