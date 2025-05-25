export interface GenerateRequest {
  prompt: string;
  seed?: number | null;
  inventory_filter?: Record<string, number> | null;
}

export const API_BASE = import.meta.env.VITE_API_URL ?? "";

function authHeaders() {
  const token = localStorage.getItem("jwt") || import.meta.env.VITE_JWT;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export function isAdmin(): boolean {
  const token = localStorage.getItem("jwt") || import.meta.env.VITE_JWT;
  if (!token) return false;
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.role === "admin";
  } catch {
    return false;
  }
}

export interface Example {
  id: string;
  title: string;
  prompt: string;
  image: string;
  tags?: string[];
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

export interface HistoryEntry {
  prompt: string;
  seed: number | null;
  result: GenerateResponse;
}

export async function generateLego(
  body: GenerateRequest,
  abortSignal?: AbortSignal
): Promise<GenerateResponse> {
  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
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
    headers: { "Content-Type": "application/json", ...authHeaders() },
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
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ comment }),
  });
  if (!res.ok) throw new Error("Failed");
}

export async function federatedSearch(query: string): Promise<{ examples: Example[] }> {
  const res = await fetch(`${API_BASE}/federated_search?q=${encodeURIComponent(query)}`);
  if (!res.ok) throw new Error("Failed");
  return (await res.json()) as { examples: Example[] };
}

export async function fetchHistory(): Promise<{ history: HistoryEntry[] }> {
  const res = await fetch(`${API_BASE}/history`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Failed");
  return (await res.json()) as { history: HistoryEntry[] };
}
