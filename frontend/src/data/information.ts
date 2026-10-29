export type InformationTopic =
  | 'help'
  | 'profile'
  | 'prompts'
  | 'terms'
  | 'privacy'
  | 'support'

type InformationContent = {
  title: string
  paragraphs: string[]
}

export const informationContent: Record<InformationTopic, InformationContent> = {
  help: {
    title: 'Comment utiliser SoprIA ?',
    paragraphs: [
      'Choisissez une opération rapide ou décrivez votre demande dans la zone de saisie. Vous pouvez aussi joindre un fichier pour préciser votre contexte.',
      'Retrouvez vos échanges dans les conversations récentes et cliquez sur « Nouvelle conversation » pour commencer un nouvel échange.',
    ],
  },
  profile: {
    title: 'Mon profil',
    paragraphs: [
      'Vous naviguez actuellement en mode démonstration. Aucun compte bancaire ni renseignement personnel n’est associé à ce profil.',
    ],
  },
  prompts: {
    title: 'Un petit guide des prompts',
    paragraphs: [
      'Précisez votre contexte, votre objectif et le format attendu.',
      'Par exemple : « Je souhaite consulter mes dernières opérations. Présente-les dans un tableau. »',
      'Ou : « Aide-moi à préparer un virement à Pierre. Quelles informations dois-je réunir ? »',
      'Ne partagez jamais votre mot de passe, votre code PIN ou un code de validation.',
    ],
  },
  terms: {
    title: 'Conditions d’utilisation',
    paragraphs: [
      'Cette interface est une démonstration de SoprIA. Elle ne permet pas d’effectuer de véritables opérations bancaires.',
      'Les conditions du service devront être mises à disposition lors de son ouverture.',
    ],
  },
  privacy: {
    title: 'Confidentialité',
    paragraphs: [
      'Les conversations de cette démonstration restent dans la mémoire de votre navigateur et sont effacées au rechargement de la page.',
      'Aucun message ni fichier joint n’est envoyé à un serveur par cette interface.',
    ],
  },
  support: {
    title: 'Contacter le support',
    paragraphs: [
      'Pour une question sur votre compte ou une urgence bancaire, contactez votre conseiller par les coordonnées habituelles de votre banque.',
      'Le support SoprIA n’est pas disponible dans cette démonstration.',
    ],
  },
}
