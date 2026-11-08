import { mockUserProfile } from './profile.mock'
import type { UserProfile } from '../types'

// Replace this adapter with the authenticated API client when a backend exists.
export async function getUserProfile(signal?: AbortSignal): Promise<UserProfile | null> {
  signal?.throwIfAborted()
  return structuredClone(mockUserProfile)
}
