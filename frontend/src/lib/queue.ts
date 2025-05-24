import {
  addQueuedGenerate,
  getQueuedGenerates,
  clearQueuedGenerates,
  setCachedGenerate,
} from './db';
import { generateLego } from '../api/lego';

export async function flushQueue(): Promise<void> {
  const requests = await getQueuedGenerates();
  if (requests.length === 0) return;
  await clearQueuedGenerates();
  for (const req of requests) {
    try {
      const res = await generateLego(req);
      const key = JSON.stringify(req);
      await setCachedGenerate(key, res);
    } catch (err) {
      console.error('flushQueue error', err);
      await addQueuedGenerate(req);
      break;
    }
  }
}
