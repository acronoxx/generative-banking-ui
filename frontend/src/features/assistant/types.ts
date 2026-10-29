import type { IconName } from '../../components/ui/Icon'

export type Message = {
  id: string
  role: 'user' | 'assistant'
  text: string
  attachmentName?: string
}

export type Conversation = {
  id: string
  title: string
  icon: IconName
  messages: Message[]
}

export type QuickAction = {
  id: string
  title: string
  description: string
  icon: IconName
  prompt: string
}
