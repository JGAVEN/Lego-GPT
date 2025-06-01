export interface GenerateRequest {
  prompt: string;
  seed?: number | null;
  inventory_filter?: Record<string, number> | null;
}

export const API_BASE = import.meta.env.VITE_API_URL ?? "";

export function authHeaders(): Record<string, string> {
  const token = localStorage.getItem("jwt") || import.meta.env.VITE_JWT;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export interface GenerateResponse {
  png_url: string;
  ldr_url: string | null;
  gltf_url: string | null;
  instructions_url: string | null;
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
    headers: { "Content-Type": "application/json", ...authHeaders() } as HeadersInit,
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

export async function detectInventory(
  body: DetectRequest,
  abortSignal?: AbortSignal
): Promise<DetectResponse> {
  const res = await fetch(`${API_BASE}/detect_inventory`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() } as HeadersInit,
    body: JSON.stringify(body),
    signal: abortSignal,
  });
  if (!res.ok) {
    throw new Error(`Request failed (${res.status})`);
  }
  return (await res.json()) as DetectResponse;
}

export async function fetchComments(exampleId: string) {
  const res = await fetch(`${API_BASE}/comments/${exampleId}`);
  if (!res.ok) throw new Error("Failed");
  const data = (await res.json()) as { comments: Array<{ user: string; text: string }> };
  return data.comments;
}

export async function postComment(exampleId: string, comment: string) {
  const res = await fetch(`${API_BASE}/comments/${exampleId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() } as HeadersInit,
    body: JSON.stringify({ comment }),
  });
  if (!res.ok) throw new Error("Failed");
}
