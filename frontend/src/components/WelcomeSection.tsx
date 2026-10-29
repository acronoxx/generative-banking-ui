import { BrandMark } from './brand/BrandMark'
import styles from './WelcomeSection.module.css'

export function WelcomeSection() {
  return (
    <section className={styles.introduction} aria-labelledby="welcome-title">
      <div>
        <h1 id="welcome-title">Bonjour, bienvenue sur SoprIA.</h1>
        <p>Votre assistant bancaire pour faire des opérations et gérer vos finances en quelques mots.</p>
      </div>
      <BrandMark className={styles.brandMark} />
    </section>
  )
}
