import { useState } from 'react'
import { InformationDialog } from '../components/InformationDialog'
import { WelcomeSection } from '../components/WelcomeSection'
import { Header } from '../components/layout/Header'
import { Footer } from '../components/layout/Footer'
import type { InformationTopic } from '../data/information'
import { ChatWorkspace } from '../features/assistant/components/ChatWorkspace'
import styles from './HomePage.module.css'

export function HomePage() {
  const [informationTopic, setInformationTopic] = useState<InformationTopic | null>(null)

  return (
    <div className="app-shell">
      <a href="#assistant-message" className={styles.skipLink}>Aller à la saisie du message</a>
      <Header
        onHelp={() => setInformationTopic('help')}
        onProfile={() => setInformationTopic('profile')}
      />
      <main id="accueil" className={`page-container ${styles.main}`}>
        <WelcomeSection />
        <ChatWorkspace onGuide={() => setInformationTopic('prompts')} />
      </main>
      <Footer onInformation={setInformationTopic} />
      <InformationDialog topic={informationTopic} onClose={() => setInformationTopic(null)} />
    </div>
  )
}
