import type { Conversation, QuickAction } from '../types'

export const initialConversations: Conversation[] = [
  { id: 'account', title: 'Mon compte', icon: 'bank', messages: [] },
  { id: 'transfer', title: 'Virement à Pierre', icon: 'transfer', messages: [] },
  { id: 'accounts', title: 'Consulter mes comptes', icon: 'bank', messages: [] },
  { id: 'statement', title: 'Demander un relevé', icon: 'file', messages: [] },
]

export const quickActions: QuickAction[] = [
  {
    id: 'accounts',
    title: 'Consulter mes comptes',
    description: 'Voir mes soldes et mes dernières opérations',
    icon: 'bank',
    prompt: 'Je souhaite consulter mes comptes et mes dernières opérations.',
  },
  {
    id: 'transfer',
    title: 'Faire un virement',
    description: 'Envoyer de l’argent à un bénéficiaire',
    icon: 'transfer',
    prompt: 'Je veux faire un virement à ',
  },
  {
    id: 'statement',
    title: 'Demander un relevé',
    description: 'Recevoir un récapitulatif de mes opérations',
    icon: 'file',
    prompt: 'Je souhaite obtenir un relevé de mes opérations.',
  },
  {
    id: 'card',
    title: 'Bloquer ma carte',
    description: 'Protéger immédiatement ma carte',
    icon: 'card-lock',
    prompt: 'Je souhaite bloquer ma carte bancaire.',
  },
]
