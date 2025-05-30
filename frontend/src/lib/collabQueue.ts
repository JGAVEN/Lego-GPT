import { addPendingCollab, getPendingCollabs, deletePendingCollab } from "./db";
import type { PendingCollab } from "./db";

export async function queueCollab(msg: PendingCollab): Promise<void> {
  await addPendingCollab(msg);
}

export async function processCollabQueue(send: (room: string, data: string) => Promise<void> | void): Promise<void> {
  const items = await getPendingCollabs();
  for (const { id, msg } of items) {
    try {
      await send(msg.room, msg.data);
      await deletePendingCollab(id);
    } catch {
      break;
    }
  }
}
