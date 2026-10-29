import { BrandMark } from './BrandMark'
import styles from './BrandLogo.module.css'

export function BrandLogo() {
  return (
    <div className={styles.logo} role="img" aria-label="Sopra Steria">
      <span>sopra</span><BrandMark /><span>steria</span>
    </div>
  )
}
