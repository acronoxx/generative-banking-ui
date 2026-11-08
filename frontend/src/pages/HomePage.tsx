import { WelcomeSection } from '../components/WelcomeSection'
import { ChatWorkspace } from '../features/assistant/components/ChatWorkspace'
import styles from './HomePage.module.css'

export function HomePage({ hidden, onGuide }: { hidden: boolean; onGuide: () => void }) {
  return (
    <main id="accueil" hidden={hidden} className={`page-container ${styles.main}`}>
      <WelcomeSection />
      <ChatWorkspace onGuide={onGuide} />
    </main>
  )
}
