import { getPendingEdits, deletePendingEdit, PendingEdit } from './db'

export async function processPendingEdits(
  send: (edit: PendingEdit) => Promise<void> | void,
): Promise<void> {
  const items = await getPendingEdits()
  for (const { id, edit } of items) {
    try {
      await send(edit)
      await deletePendingEdit(id)
    } catch {
      break
    }
  }
}
