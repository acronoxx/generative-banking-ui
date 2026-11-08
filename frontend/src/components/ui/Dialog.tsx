import { useEffect, useId, useRef } from 'react'
import type { ReactNode } from 'react'
import { Icon } from './Icon'
import styles from '../InformationDialog.module.css'

type DialogProps = { open: boolean; title: string; onClose: () => void; children: ReactNode }

export function Dialog({ open, title, onClose, children }: DialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null)
  const titleId = useId()

  useEffect(() => {
    const dialog = dialogRef.current
    if (open && dialog && !dialog.open) dialog.showModal()
    if (!open && dialog?.open) dialog.close()
  }, [open])

  return (
    <dialog ref={dialogRef} className={styles.dialog} onCancel={onClose} aria-labelledby={titleId}
      onClick={(event) => {
        const rect = event.currentTarget.getBoundingClientRect()
        if (event.target === event.currentTarget && (
          event.clientX < rect.left || event.clientX > rect.right ||
          event.clientY < rect.top || event.clientY > rect.bottom
        )) onClose()
      }}>
      {open && <>
        <div className={styles.heading}>
          <h2 id={titleId}>{title}</h2>
          <button type="button" className="icon-button" onClick={onClose} aria-label="Fermer"><Icon name="close" /></button>
        </div>
        {children}
      </>}
    </dialog>
  )
}
