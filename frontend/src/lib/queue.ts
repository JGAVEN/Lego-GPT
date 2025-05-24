import { addQueuedGenerate, getQueuedGenerates, clearQueuedGenerates, setCachedGenerate } from './db';
import type { GenerateResponse } from '../api/lego';
import { generateLego } from '../api/lego';

export async function flushQueue(): Promise<void> {
  const requests = await getQueuedGenerates();
  if (requests.length === 0) return;
  await clearQueuedGenerates();
  for (const req of requests) {
    try {
      const res: GenerateResponse = await generateLego(req);
      const key = JSON.stringify(req);
      await setCachedGenerate(key, res);
    } catch (error) {
      console.error('Failed to flush queued request', error);
      await addQueuedGenerate(req);
      break;
    }
  }
}
