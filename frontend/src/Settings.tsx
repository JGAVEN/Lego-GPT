import { useEffect, useState } from "react";
import {
  countCachedGenerates,
  countPendingGenerates,
  clearCachedGenerates,
  clearPendingGenerates,
} from "./lib/db";

export default function Settings({ onBack }: { onBack: () => void }) {
  const [cacheCount, setCacheCount] = useState(0);
  const [queueCount, setQueueCount] = useState(0);

  async function refresh() {
    setCacheCount(await countCachedGenerates());
    setQueueCount(await countPendingGenerates());
  }

  useEffect(() => {
    refresh();
  }, []);

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      <p>Cached results: {cacheCount}</p>
      <p>Queued requests: {queueCount}</p>
      <div className="mt-4 space-x-2">
        <button
          className="bg-gray-200 px-3 py-1 rounded"
          onClick={async () => {
            await clearCachedGenerates();
            refresh();
          }}
        >
          Clear Cache
        </button>
        <button
          className="bg-gray-200 px-3 py-1 rounded"
          onClick={async () => {
            await clearPendingGenerates();
            refresh();
          }}
        >
          Clear Queue
        </button>
      </div>
      <button className="mt-6 text-blue-600 underline" onClick={onBack}>
        Back
      </button>
    </main>
  );
}
