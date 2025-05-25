import { useEffect, useState } from "react";
import { API_BASE } from "./api/lego";

export default function Analytics({ onBack }: { onBack: () => void }) {
  const [data, setData] = useState<{ [k: string]: number }>({});
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
            {k}: {v}
          </li>
        ))}
      </ul>
      <button className="underline" onClick={onBack} aria-label="back">
        Back
      </button>
    </main>
  );
}
