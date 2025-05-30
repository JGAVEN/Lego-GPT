import { API_BASE } from "../api/lego";
import type { DetectResponse } from "../api/lego";
import {
  getPendingDetects,
  deletePendingDetect,
  setCachedDetect,
} from "./db";
import type { PendingDetect } from "./db";

async function runDetect(req: PendingDetect): Promise<DetectResponse> {
  const res = await fetch(`${API_BASE}/detect_inventory`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: req.image }),
  });
  if (!res.ok) {
    throw new Error(`Request failed (${res.status})`);
  }
  const { job_id } = (await res.json()) as { job_id: string };
  while (true) {
    const poll = await fetch(`${API_BASE}/detect_inventory/${job_id}`);
    if (poll.status === 200) {
      return (await poll.json()) as DetectResponse;
    }
    if (poll.status !== 202) {
      throw new Error(`Job failed (${poll.status})`);
    }
    await new Promise((r) => setTimeout(r, 1000));
  }
}

export async function processDetectQueue(): Promise<void> {
  const items = await getPendingDetects();
  for (const { id, request } of items) {
    try {
      const result = await runDetect(request);
      await setCachedDetect(request.image, result);
      await deletePendingDetect(id);
    } catch {
      break;
    }
  }
}
