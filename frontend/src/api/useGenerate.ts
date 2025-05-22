import { useEffect, useState } from "react";
import type { GenerateRequest, GenerateResponse } from "./lego";

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
  seed: number | null | undefined
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
      try {
        const reqBody: GenerateRequest = { prompt };
        if (seed !== undefined && seed !== null) {
          reqBody.seed = seed;
        }
        const res = await fetch("/generate", {
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
          const poll = await fetch(`/generate/${job_id}`, {
            signal: ctrl.signal,
          });
          if (poll.status === 200) {
            const result = (await poll.json()) as GenerateResponse;
            if (!cancelled) {
              setData(result);
            }
            break;
          }
          if (poll.status !== 202) {
            throw new Error(`Job failed (${poll.status})`);
          }
          await new Promise((r) => setTimeout(r, 1000));
        }
      } catch (err: any) {
        if (!cancelled && err.name !== "AbortError") {
          setError(err.message ?? "Unknown error");
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
  }, [prompt, seed]);

  return { data, loading, error };
}
