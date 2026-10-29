import type { ReactNode, SVGProps } from 'react'

export type IconName =
  | 'agent' | 'arrow-up' | 'arrow-right' | 'arrow-up-right' | 'bank'
  | 'card-lock' | 'check' | 'chevron-down' | 'close' | 'file'
  | 'help' | 'lightbulb' | 'paperclip' | 'plus' | 'search' | 'transfer' | 'user'

const paths: Record<IconName, ReactNode> = {
  agent: <><circle cx="12" cy="7" r="3" /><path d="M6 9V7a6 6 0 0 1 12 0v2M5 8v4h3V8zm11 0v4h3V8zM12 14c-4 0-7 2-7 5v3h14v-3c0-3-3-5-7-5ZM18 12c0 2-2 2-4 2" /></>,
  'arrow-up': <path d="M12 20V4m-6 6 6-6 6 6" />,
  'arrow-right': <path d="M4 12h16m-6-6 6 6-6 6" />,
  'arrow-up-right': <path d="M6 18 18 6M7 6h11v11" />,
  bank: <path d="m2 8 10-6 10 6H2Zm0 14h20M3 19h18M5 10v7m5-7v7m4-7v7m5-7v7" />,
  'card-lock': <path d="M13 18H3a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h17a1 1 0 0 1 1 1v5M2 8h19M5 13h5M16 15v-2a2 2 0 0 1 4 0v2m-6 0h8v7h-8zM18 18v1" />,
  check: <path d="m5 12 4 4L19 6" />,
  'chevron-down': <path d="m5 9 7 7 7-7" />,
  close: <path d="m6 6 12 12M6 18 18 6" />,
  file: <path d="M5 2h10l5 5v15H5V2Zm10 0v6h5M8 11h3m-3 4h3m-3 4h3m3-6 1 1 2-2m-3 5 1 1 2-2" />,
  help: <><circle cx="12" cy="12" r="10" /><path d="M9 8a3 3 0 0 1 6 1c0 2-3 2-3 4m0 4v.1" /></>,
  lightbulb: <path d="M9 18h6m-5 3h4m-5-5c0-2-3-3-3-7a6 6 0 0 1 12 0c0 4-3 5-3 7H9Zm3 0v-5m-2-3 2 3 2-3" />,
  paperclip: <path d="m8 13 7-7a3 3 0 0 1 4 4L9 20a5 5 0 0 1-7-7L13 2a3.5 3.5 0 0 1 5 5L8 17a2 2 0 0 1-3-3l9-9" />,
  plus: <path d="M12 3v18M3 12h18" />,
  search: <><circle cx="10" cy="10" r="6" /><path d="m15 15 6 6" /></>,
  transfer: <><path d="M2 6h19m-4-4 4 4-4 4M22 18H3m4-4-4 4 4 4" /><circle cx="11" cy="12" r="4" /></>,
  user: <><circle cx="12" cy="7" r="4" /><path d="M5 21v-2a7 7 0 0 1 14 0v2" /></>,
}

type IconProps = SVGProps<SVGSVGElement> & { name: IconName; size?: number }

export function Icon({ name, size = 20, ...props }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"
      strokeLinejoin="round" aria-hidden="true" {...props}>
      {paths[name]}
    </svg>
  )
}
