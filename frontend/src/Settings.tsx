import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  countCachedGenerates,
  clearGenerateCache,
  countQueuedGenerates,
  clearQueuedGenerates,
} from './lib/db';
import { flushQueue } from './lib/queue';

export default function Settings() {
  const [cacheCount, setCacheCount] = useState(0);
  const [queueCount, setQueueCount] = useState(0);

  async function refresh() {
    setCacheCount(await countCachedGenerates());
    setQueueCount(await countQueuedGenerates());
  }

  useEffect(() => {
    refresh();
  }, []);

  async function handleClearCache() {
    await clearGenerateCache();
    refresh();
  }

  async function handleFlushQueue() {
    await flushQueue();
    refresh();
  }

  async function handleClearQueue() {
    await clearQueuedGenerates();
    refresh();
  }

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      <p className="mb-2">Cached results: {cacheCount}</p>
      <p className="mb-4">Queued requests: {queueCount}</p>
      <div className="space-x-4 mb-4">
        <button onClick={handleClearCache} className="bg-blue-600 text-white px-3 py-2 rounded">
          Clear Cache
        </button>
        <button onClick={handleFlushQueue} className="bg-blue-600 text-white px-3 py-2 rounded">
          Flush Queue
        </button>
        <button onClick={handleClearQueue} className="bg-blue-600 text-white px-3 py-2 rounded">
          Clear Queue
        </button>
      </div>
      <Link to="/" className="text-blue-600 underline">
        Back
      </Link>
    </main>
  );
}
