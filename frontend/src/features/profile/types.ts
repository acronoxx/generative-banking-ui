export interface PersonalInformation {
  firstName: string
  lastName: string
  legalName: string
  birthDate: string
  birthPlace: string
  email: string
  emailVerified: boolean
  phone: string
  phoneVerified: boolean
  address: string
  identityVerified: boolean
  updatedAt: string
}

export type ProfileContact = Pick<PersonalInformation, 'email' | 'phone' | 'address'>

export interface BankAccount {
  id: string
  kind: 'current' | 'savings'
  name: string
  maskedNumber?: string
  description?: string
}

export interface BankCard {
  id: string
  name: string
  lastFour: string
  expiresAt: string
  active: boolean
}

export interface PaymentLimit {
  total: number
  used: number
  currency: string
  rollingDays: number
}

export interface CustomerPreferences {
  contactless: boolean
  contactlessLimit: number
  internationalZone: string
  onlinePayments: boolean
}

export interface SecuritySettings {
  deviceName: string
  lastValidation: string
  codeUpdatedAt: string
  trustedContactName: string | null
}

export interface BankingAdvisor {
  name: string
  initials: string
  role: string
  agency: string
  available: boolean
}

export interface UserProfile {
  id: string
  clientReference: string
  agency: string
  certified: boolean
  personal: PersonalInformation
  accounts: BankAccount[]
  card: BankCard | null
  paymentLimit: PaymentLimit | null
  preferences: CustomerPreferences
  security: SecuritySettings
  advisor: BankingAdvisor | null
  support: { name: string; hours: string }
}
