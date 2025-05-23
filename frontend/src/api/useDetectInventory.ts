import { useEffect, useState } from "react";
import type { DetectRequest, DetectResponse } from "./lego";

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

    const ctrl = new AbortController();
    let cancelled = false;

    async function run() {
      setLoading(true);
      setError(null);
      setData(null);
      try {
        const body: DetectRequest = { image };
        const res = await fetch("/detect_inventory", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
          signal: ctrl.signal,
        });
        if (!res.ok) {
          throw new Error(`Request failed (${res.status})`);
        }
        const { job_id } = (await res.json()) as { job_id: string };
        while (!cancelled) {
          const poll = await fetch(`/detect_inventory/${job_id}`, {
            signal: ctrl.signal,
          });
          if (poll.status === 200) {
            const result = (await poll.json()) as DetectResponse;
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
  }, [image]);

  return { data, loading, error };
}
