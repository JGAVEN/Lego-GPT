export interface GenerateRequest {
  prompt: string;
  seed?: number | null;
}

export interface GenerateResponse {
  png: string;          // base-64 PNG
  ldr?: string;         // reserved for future use
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
