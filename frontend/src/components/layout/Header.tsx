import { BrandLogo } from '../brand/BrandLogo'
import { Icon } from '../ui/Icon'
import styles from './Header.module.css'

type HeaderProps = { onHelp: () => void; activePage: 'home' | 'profile' }

export function Header({ onHelp, activePage }: HeaderProps) {
  return (
    <header className={styles.header}>
      <div className={`page-container ${styles.inner}`}>
        <a href="#/accueil" className={styles.brand} aria-label="SoprIA — Accueil">
          <BrandLogo /><span className={styles.divider} /><span className={styles.product}>SoprIA</span>
        </a>
        <nav className={styles.navigation} aria-label="Navigation principale">
          <a href="#/accueil" className={activePage === 'home' ? styles.active : undefined} aria-current={activePage === 'home' ? 'page' : undefined}>Accueil</a>
          <a href="#/profil" className={activePage === 'profile' ? styles.active : undefined} aria-current={activePage === 'profile' ? 'page' : undefined}>Profil</a>
        </nav>
        <div className={styles.actions}>
          <button type="button" className={styles.help} onClick={onHelp} aria-label="Aide et FAQ"><Icon name="help" size={18} />Aide</button>
          <span className={styles.divider} />
          <a href="#/profil" className={styles.profile} aria-label="Ouvrir mon profil">
            <Icon name="user" size={18} />
          </a>
        </div>
      </div>
    </header>
  )
}
