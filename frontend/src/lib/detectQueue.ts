// File: frontend/src/lib/detectQueue.ts

import { authHeaders, API_BASE } from "../api/lego";
import { getPendingDetects, deletePendingDetect, setCachedDetect } from "./db";
import type { PendingDetect } from "./db";

async function runDetect(req: PendingDetect): Promise<DetectResponse> {
  // Send the initial POST to kick off detection, including the JWT
  const res = await fetch(`${API_BASE}/detect_inventory`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ image: req.image }),
  });
  if (!res.ok) {
    throw new Error(`Request failed (${res.status})`);
  }

  // Extract job_id from the response
  const { job_id } = (await res.json()) as { job_id: string };

  // Poll the job status with exponential backoff
  let delay = 2000; // Start at 2 seconds
  const maxDelay = 30000; // Cap at 30 seconds

  while (true) {
    const poll = await fetch(`${API_BASE}/detect_inventory/${job_id}`, {
      method: "GET",
      headers: { ...authHeaders() },
    });

    if (poll.status === 200) {
      // Job complete: return the parsed result
      return (await poll.json()) as DetectResponse;
    }

    if (poll.status !== 202) {
      // Unexpected status: treat as failure
      throw new Error(`Job failed (${poll.status})`);
    }

    // Wait for the current delay, then double it (up to maxDelay)
    await new Promise((r) => setTimeout(r, delay));
    delay = Math.min(delay * 2, maxDelay);
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
      // If an error occurs (offline, rate limit, etc.), stop processing further items
      break;
    }
  }
}
