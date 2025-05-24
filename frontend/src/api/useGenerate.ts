import { useEffect, useState } from "react";
import type { GenerateRequest, GenerateResponse } from "./lego";
import { generateLego } from "./lego";
import {
  getCachedGenerate,
  setCachedGenerate,
  addQueuedGenerate,
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

    const ctrl = new AbortController();
    let cancelled = false;

    async function run() {
      setLoading(true);
      setError(null);
      setData(null);
      const cacheKey = JSON.stringify({ prompt, seed, inventoryFilter });
      const cached = await getCachedGenerate(cacheKey);
      const reqBody: GenerateRequest = { prompt };
      if (seed !== undefined && seed !== null) {
        reqBody.seed = seed;
      }
      if (inventoryFilter) {
        reqBody.inventory_filter = inventoryFilter;
      }
      try {
        const result = await generateLego(reqBody, ctrl.signal);
        if (!cancelled) {
          setData(result);
          await setCachedGenerate(cacheKey, result);
        }
      } catch (err: unknown) {
        if (!cancelled) {
          if (!navigator.onLine) {
            await addQueuedGenerate(reqBody);
            if (cached) {
              setData(cached);
              setError("Offline - request queued, showing cached result");
            } else {
              setError("Offline - request queued");
            }
          } else if (cached) {
            setData(cached);
            setError("Offline - showing cached result");
          } else if (err instanceof Error && err.name !== "AbortError") {
            setError(err.message);
          } else {
            setError("Unknown error");
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
