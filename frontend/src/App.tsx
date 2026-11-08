import { useEffect, useState, useSyncExternalStore } from 'react'
import { Header } from './components/layout/Header'
import { Footer } from './components/layout/Footer'
import { InformationDialog } from './components/InformationDialog'
import type { InformationTopic } from './data/information'
import { HomePage } from './pages/HomePage'
import { ProfilePage } from './pages/ProfilePage'
import styles from './App.module.css'

function subscribeToNavigation(callback: () => void) {
  window.addEventListener('hashchange', callback)
  return () => window.removeEventListener('hashchange', callback)
}

function getRoute() { return window.location.hash }

export default function App() {
  const route = useSyncExternalStore(subscribeToNavigation, getRoute)
  const activePage = route.split('/')[1] === 'profil' ? 'profile' : 'home'
  const [informationTopic, setInformationTopic] = useState<InformationTopic | null>(null)

  useEffect(() => {
    document.title = activePage === 'profile' ? 'Mon profil | SoprIA' : 'Accueil | SoprIA'
    const section = route.split('/')[2]
    // ProfilePage waits for its data before focusing a directly linked section.
    if (section && activePage === 'profile') return
    const target = document.querySelector<HTMLElement>('main:not([hidden]) h1')
    // Hash routes also support direct links, browser back and keyboard navigation.
    target?.focus({ preventScroll: true })
    if (route.startsWith('#/')) window.scrollTo(0, 0)
  }, [route, activePage])

  return (
    <div className="app-shell">
      <a href={activePage === 'home' ? '#assistant-message' : '#profile-title'} className={styles.skipLink} onClick={(event) => {
        event.preventDefault()
        const target = document.getElementById(activePage === 'home' ? 'assistant-message' : 'profile-title')
        target?.focus()
        target?.scrollIntoView({ block: 'center' })
      }}>
        {activePage === 'home' ? 'Aller à la saisie du message' : 'Aller au contenu du profil'}
      </a>
      <Header activePage={activePage} onHelp={() => setInformationTopic('help')} />
      <HomePage hidden={activePage !== 'home'} onGuide={() => setInformationTopic('prompts')} />
      <ProfilePage hidden={activePage !== 'profile'} section={route.split('/')[2] || ''} onInformation={setInformationTopic} />
      <Footer onInformation={setInformationTopic} />
      <InformationDialog topic={informationTopic} onClose={() => setInformationTopic(null)} />
    </div>
  )
}
