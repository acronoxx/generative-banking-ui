type BrandMarkProps = { className?: string }

export function BrandMark({ className }: BrandMarkProps) {
  return (
    <svg className={className} width="48" height="38" viewBox="0 0 48 38" fill="none" aria-hidden="true">
      <path d="M12 6C17 2 32 0 39 3c5 2 7 8 5 12-2 4-15-2-32-9Z" fill="#d7193f" />
      <path d="M36 32c-5 4-20 6-27 3-5-2-7-8-5-12 2-4 15 2 32 9Z" fill="#d7193f" />
      <path d="M12 6C1 4-4 10 10 18 4 12 8 8 12 6ZM36 32c11 2 16-4 2-12 6 6 2 10-2 12Z" fill="#f58220" />
    </svg>
  )
}
