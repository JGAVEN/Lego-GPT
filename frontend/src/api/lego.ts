export interface GenerateRequest {
  prompt: string;
  seed?: number | null;
}

export interface GenerateResponse {
  png_url: string;
  ldr_url: string | null;
  brick_counts: Record<string, number>;
}

export async function generateLego(
  body: GenerateRequest,
  abortSignal?: AbortSignal
): Promise<GenerateResponse> {
  const res = await fetch("/generate", {
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
  return (await res.json()) as GenerateResponse;
}
