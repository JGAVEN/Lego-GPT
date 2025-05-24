export interface GenerateRequest {
  prompt: string;
  seed?: number | null;
  inventory_filter?: Record<string, number> | null;
}

export const API_BASE = import.meta.env.VITE_API_URL ?? "";

export interface GenerateResponse {
  png_url: string;
  ldr_url: string | null;
  gltf_url: string | null;
  brick_counts: Record<string, number>;
}

export interface DetectRequest {
  image: string;
}

export interface DetectResponse {
  brick_counts: Record<string, number>;
}

export async function generateLego(
  body: GenerateRequest,
  abortSignal?: AbortSignal
): Promise<GenerateResponse> {
  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal: abortSignal,
  });

  if (!res.ok) {
    throw new Error(
      `Request failed (${res.status}). ` +
        "Is the backend running? Try `docker compose up` in the repo root."
    );
  }
  const { job_id } = (await res.json()) as { job_id: string };
  while (true) {
    const poll = await fetch(`${API_BASE}/generate/${job_id}`, {
      signal: abortSignal,
    });
    if (poll.status === 200) {
      return (await poll.json()) as GenerateResponse;
    }
    if (poll.status !== 202) {
      throw new Error(`Job failed (${poll.status})`);
    }
    await new Promise((r) => setTimeout(r, 1000));
  }
}

export async function detectInventory(
  body: DetectRequest,
  abortSignal?: AbortSignal
): Promise<DetectResponse> {
  const res = await fetch(`${API_BASE}/detect_inventory`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal: abortSignal,
  });
  if (!res.ok) {
    throw new Error(`Request failed (${res.status})`);
  }
  return (await res.json()) as DetectResponse;
}
