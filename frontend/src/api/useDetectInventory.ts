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
        // Kick off the detect_inventory job
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

        // Extract the job_id from the response
        const { job_id } = (await res.json()) as { job_id: string };

        // Prevent overlapping polling loops
        if ((window as any)._detectIsRunning) {
          throw new Error("Detect is already in progress");
        }
        (window as any)._detectIsRunning = true;

        try {
          // Begin polling with exponential backoff
          let delay = 2000;      // Start with a 2-second delay
          const maxDelay = 30000; // Cap delay at 30 seconds

          // Initial wait before sending the first GET
          await new Promise((r) => setTimeout(r, delay));
          delay = Math.min(delay * 2, maxDelay);

          while (!cancelled) {
            const poll = await fetch(`${API_BASE}/detect_inventory/${job_id}`, {
              method: "GET",
              headers: { ...authHeaders() },
              signal: ctrl.signal,
            });

            if (poll.status === 200) {
              // Job is complete
              const result = (await poll.json()) as DetectResponse;
              if (!cancelled) {
                setData(result);
                await setCachedDetect(cacheKey, result);
              }
              break;
            }

            if (poll.status !== 202) {
              // An unexpected status code; treat as failure
              throw new Error(`Job failed (${poll.status})`);
            }

            // Wait for the current delay, then double it (up to the max)
            await new Promise((r) => setTimeout(r, delay));
            delay = Math.min(delay * 2, maxDelay);
          }
        } finally {
          delete (window as any)._detectIsRunning;
        }
      } catch (err: unknown) {
        if (!cancelled) {
          if (cached) {
            // Show cached result if available
            setData(cached);
            setError("Offline - showing cached result");
          } else {
            // Queue the request for later
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
