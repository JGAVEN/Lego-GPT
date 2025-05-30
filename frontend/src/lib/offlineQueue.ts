import { API_BASE } from "../api/lego";
import type { GenerateResponse } from "../api/lego";
import {
  getPendingGenerates,
  deletePendingGenerate,
  setCachedGenerate,
} from "./db";
import type { PendingRequest } from "./db";

async function runGenerate(req: PendingRequest): Promise<GenerateResponse> {
  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt: req.prompt,
      seed: req.seed,
      inventory_filter: req.inventory_filter ?? undefined,
    }),
  });
  if (!res.ok) {
    throw new Error(`Request failed (${res.status})`);
  }
  const { job_id } = (await res.json()) as { job_id: string };
  while (true) {
    const poll = await fetch(`${API_BASE}/generate/${job_id}`);
    if (poll.status === 200) {
      return (await poll.json()) as GenerateResponse;
    }
    if (poll.status !== 202) {
      throw new Error(`Job failed (${poll.status})`);
    }
    await new Promise((r) => setTimeout(r, 1000));
  }
}

export async function processPending(): Promise<void> {
  const items = await getPendingGenerates();
  for (const { id, request } of items) {
    try {
      const result = await runGenerate(request);
      const key = JSON.stringify({
        prompt: request.prompt,
        seed: request.seed,
        inventoryFilter: request.inventory_filter,
      });
      await setCachedGenerate(key, result);
      await deletePendingGenerate(id);
    } catch {
      break; // stop if offline or failed
    }
  }
}
