import { useEffect, useState } from "react";
import { API_BASE } from "./api/lego";

interface Metrics {
  history?: {
    token_usage: Array<[number, number]>;
    rate_limit_hits: Array<[number, number]>;
  };
  [k: string]: number | Record<string, unknown> | undefined;
}

export default function Analytics({ onBack }: { onBack: () => void }) {
  const [data, setData] = useState<Metrics>({});
  useEffect(() => {
    fetch(`${API_BASE}/metrics`)
      .then((res) => res.json())
      .then((d) => setData(d))
      .catch(() => setData({}));
  }, []);
  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">Analytics</h1>
      <ul className="mb-4">
        {Object.entries(data).map(([k, v]) => (
          <li key={k} className="text-sm">
            {k}: {JSON.stringify(v)}
          </li>
        ))}
      </ul>
      {data.history && (
        <div className="text-sm mb-4">
          <p>Token usage (last hour):</p>
          <div>
            {data.history.token_usage.map(([ts, v]) => (
              <span key={ts} className="inline-block w-1 bg-blue-600 mr-0.5" style={{ height: `${v}px` }} />
            ))}
          </div>
          <p className="mt-2">Rate-limit hits:</p>
          <div>
            {data.history.rate_limit_hits.map(([ts, v]) => (
              <span key={ts} className="inline-block w-1 bg-red-600 mr-0.5" style={{ height: `${v}px` }} />
            ))}
          </div>
        </div>
      )}
      <button className="underline" onClick={onBack} aria-label="back">
        Back
      </button>
    </main>
  );
}
