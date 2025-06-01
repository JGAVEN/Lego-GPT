import { useEffect, useState } from "react";
import type { DetectRequest, DetectResponse } from "./lego";
import { API_BASE, authHeaders } from "./lego";
import {
  getCachedDetect,
  setCachedDetect,
  addPendingDetect,
} from "../lib/db";

export interface UseDetectResult {
  data: DetectResponse | null;
  loading: boolean;
  error: string | null;
}

export default function useDetectInventory(image: string | null): UseDetectResult {
  const [data, setData] = useState<DetectResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!image) return;

    const img = image;
    const ctrl = new AbortController();
    let cancelled = false;

    async function run() {
      setLoading(true);
      setError(null);
      setData(null);
      const cacheKey = img;
      const cached = await getCachedDetect(cacheKey);

      try {
        const body: DetectRequest = { image: img };
        const res = await fetch(`${API_BASE}/detect_inventory`, {
          method: "POST",
          headers: { "Content-Type": "application/json", ...authHeaders() },
          body: JSON.stringify(body),
          signal: ctrl.signal,
        });

        if (!res.ok) {
          throw new Error(`Request failed (${res.status})`);
        }

        const { job_id } = (await res.json()) as { job_id: string };
        while (!cancelled) {
          const poll = await fetch(`${API_BASE}/detect_inventory/${job_id}`, {
            method: "GET",
            headers: { ...authHeaders() },
            signal: ctrl.signal,
          });

          if (poll.status === 200) {
            const result = (await poll.json()) as DetectResponse;
            if (!cancelled) {
              setData(result);
              await setCachedDetect(cacheKey, result);
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
            await addPendingDetect({ image: img });
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
  }, [image]);

  return { data, loading, error };
}
