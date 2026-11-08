import type { UserProfile } from '../types'

// Entirely fictional fixtures. No valid account number, credentials or real contact details.
export const mockUserProfile: UserProfile = {
  id: 'demo-client-001',
  clientReference: 'DEMO 0001 22',
  agency: 'Paris Opéra (75009)',
  certified: true,
  personal: {
    firstName: 'Claire', lastName: 'Laurent', legalName: 'Claire Marie Laurent',
    birthDate: '1988-09-18', birthPlace: 'Lyon (69002)',
    email: 'claire.laurent@example.com', emailVerified: true,
    phone: '+33 6 XX XX XX 78', phoneVerified: true,
    address: '14, rue de la Démonstration, 75009 Paris (France)',
    identityVerified: true, updatedAt: '2026-01-14',
  },
  accounts: [
    { id: 'demo-current', kind: 'current', name: 'Compte Courant Particulier', maskedNumber: 'FR•• •••• •••• •••• •••• ••01' },
    { id: 'demo-savings', kind: 'savings', name: 'Livret A Solidaire', description: 'Rémunération réglementée — exemple' },
  ],
  card: { id: 'demo-card', name: 'Visa Premier', lastFour: '4892', expiresAt: '09/28', active: true },
  paymentLimit: { total: 3000, used: 850, currency: 'EUR', rollingDays: 7 },
  preferences: { contactless: true, contactlessLimit: 50, internationalZone: 'Zone Euro & International', onlinePayments: true },
  security: {
    deviceName: 'iPhone 15 Pro (démo)', lastValidation: '2026-01-14T09:14:00+01:00',
    codeUpdatedAt: '2025-11-30', trustedContactName: null,
  },
  advisor: {
    name: 'Marc Dupont', initials: 'MD', role: 'Banque Privée & Patrimoine',
    agency: 'Agence Paris Opéra (75009)', available: true,
  },
  support: { name: 'Assistance SoprIA Banque Privée', hours: 'Du lundi au vendredi de 8h30 à 19h00 (horaires de démonstration).' },
}
