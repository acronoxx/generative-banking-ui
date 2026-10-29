import { BrandLogo } from '../brand/BrandLogo'
import { Icon } from '../ui/Icon'
import styles from './Header.module.css'

type HeaderProps = { onHelp: () => void; onProfile: () => void }

export function Header({ onHelp, onProfile }: HeaderProps) {
  return (
    <header className={styles.header}>
      <div className={`page-container ${styles.inner}`}>
        <a href="#accueil" className={styles.brand} aria-label="SoprIA — Accueil">
          <BrandLogo /><span className={styles.divider} /><span className={styles.product}>SoprIA</span>
        </a>
        <nav className={styles.navigation} aria-label="Navigation principale">
          <a href="#accueil" className={styles.active} aria-current="page">Accueil</a>
          <button type="button" onClick={onProfile}>Profil</button>
        </nav>
        <div className={styles.actions}>
          <button type="button" className={styles.help} onClick={onHelp}><Icon name="help" size={18} />Aide</button>
          <span className={styles.divider} />
          <button type="button" className={styles.profile} onClick={onProfile} aria-label="Ouvrir mon profil">
            <Icon name="user" size={18} />
          </button>
        </div>
      </div>
    </header>
  )
}
