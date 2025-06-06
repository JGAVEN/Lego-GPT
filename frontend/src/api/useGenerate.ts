import { useEffect, useState } from "react";
import type { GenerateRequest, GenerateResponse } from "./lego";
import { API_BASE } from "./lego";
import {
  getCachedGenerate,
  setCachedGenerate,
  addPendingGenerate,
} from "../lib/db";

export interface UseGenerateResult {
  data: GenerateResponse | null;
  loading: boolean;
  error: string | null;
}

/**
 * Generate a Lego model based on the prompt and seed.
 * When `prompt` is falsy, the hook does nothing.
 */
export default function useGenerate(
  prompt: string | null,
  seed: number | null | undefined,
  inventoryFilter: Record<string, number> | null = null
): UseGenerateResult {
  const [data, setData] = useState<GenerateResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!prompt) return;

    const actualPrompt = prompt;

    const ctrl = new AbortController();
    let cancelled = false;

    async function run() {
      setLoading(true);
      setError(null);
      setData(null);
      const cacheKey = JSON.stringify({ prompt: actualPrompt, seed, inventoryFilter });
      const cached = await getCachedGenerate(cacheKey);
      try {
        const reqBody: GenerateRequest = { prompt: actualPrompt };
        if (seed !== undefined && seed !== null) {
          reqBody.seed = seed;
        }
        if (inventoryFilter) {
          reqBody.inventory_filter = inventoryFilter;
        }
        const res = await fetch(`${API_BASE}/generate`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(reqBody),
          signal: ctrl.signal,
        });
        if (!res.ok) {
          throw new Error(`Request failed (${res.status})`);
        }
        const { job_id } = (await res.json()) as { job_id: string };

        while (!cancelled) {
          const poll = await fetch(`${API_BASE}/generate/${job_id}`, {
            signal: ctrl.signal,
          });
          if (poll.status === 200) {
            const result = (await poll.json()) as GenerateResponse;
            if (!cancelled) {
              setData(result);
              await setCachedGenerate(cacheKey, result);
            }
            break;
          }
          if (poll.status !== 202) {
            throw new Error(`Job failed (${poll.status})`);
          }
          await new Promise((r) => setTimeout(r, 1000));
        }
        } catch (err: unknown) {
          if (!cancelled) {
            if (cached) {
              setData(cached);
              setError("Offline - showing cached result");
            } else {
              await addPendingGenerate({
                prompt: actualPrompt,
                seed: seed ?? null,
                inventory_filter: inventoryFilter,
              });
              if (err instanceof Error && err.name !== "AbortError") {
                setError("Offline - request queued");
              } else {
                setError("Unknown error");
              }
            }
          }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    run();
    return () => {
      cancelled = true;
      ctrl.abort();
    };
  }, [prompt, seed, inventoryFilter]);

  return { data, loading, error };
}
