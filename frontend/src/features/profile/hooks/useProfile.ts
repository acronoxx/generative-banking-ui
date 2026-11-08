import { useEffect, useState } from 'react'
import { getUserProfile } from '../data/profile.repository'
import type { ProfileContact, UserProfile } from '../types'

type ProfileState =
  | { status: 'loading' }
  | { status: 'error' }
  | { status: 'ready'; profile: UserProfile | null }

export function useProfile() {
  const [state, setState] = useState<ProfileState>({ status: 'loading' })
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    getUserProfile(controller.signal).then((profile) => {
      if (!controller.signal.aborted) setState({ status: 'ready', profile })
    }).catch(() => {
      if (!controller.signal.aborted) setState({ status: 'error' })
    })
    return () => controller.abort()
  }, [attempt])

  function retry() {
    setState({ status: 'loading' })
    setAttempt((value) => value + 1)
  }

  function updateContact(contact: ProfileContact) {
    setState((current) => {
      if (current.status !== 'ready' || !current.profile) return current
      const personal = current.profile.personal
      return {
        status: 'ready',
        profile: {
          ...current.profile,
          personal: {
            ...personal, ...contact,
            // Local edits cannot certify a new email or link a new phone to a security device.
            emailVerified: contact.email === personal.email && personal.emailVerified,
            phoneVerified: contact.phone === personal.phone && personal.phoneVerified,
            updatedAt: new Date().toISOString().slice(0, 10),
          },
        },
      }
    })
  }

  return { state, retry, updateContact }
}
