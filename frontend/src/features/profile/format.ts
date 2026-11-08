export function formatDate(value: string, long = false) {
  return new Intl.DateTimeFormat('fr-FR', {
    dateStyle: long ? 'long' : 'short', timeZone: 'Europe/Paris',
  }).format(new Date(value))
}

export function formatMoney(value: number, currency = 'EUR') {
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency }).format(value)
}
