import { useEffect, useState } from "react";
import { useI18n } from "./i18n";
import {
  countCachedGenerates,
  countPendingGenerates,
  clearCachedGenerates,
  clearPendingGenerates,
  countPendingCollabs,
  clearPendingCollabs,
} from "./lib/db";
import { hasSubscription, subscribe, unsubscribe } from "./lib/push";

export default function Settings({ onBack }: { onBack: () => void }) {
  const { t } = useI18n();
  const [cacheCount, setCacheCount] = useState(0);
  const [queueCount, setQueueCount] = useState(0);
  const [editCount, setEditCount] = useState(0);
  const [push, setPush] = useState(false);

  async function refresh() {
    setCacheCount(await countCachedGenerates());
    setQueueCount(await countPendingGenerates());
    setEditCount(await countPendingCollabs());
    setPush(await hasSubscription());
  }

  useEffect(() => {
    refresh();
  }, []);

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">{t("settings")}</h1>
      <p>{t("cachedResults")} {cacheCount}</p>
      <p>{t("queuedRequests")} {queueCount}</p>
      <p>{t("pendingEdits")} {editCount}</p>
      <p>{push ? t("pushEnabled") : ""}</p>
      <div className="mt-4 space-x-2">
        <button
          className="bg-gray-200 px-3 py-1 rounded"
          onClick={async () => {
            await clearCachedGenerates();
            refresh();
          }}
          aria-label="clear cache"
        >
          {t("clearCache")}
        </button>
        <button
          className="bg-gray-200 px-3 py-1 rounded"
          onClick={async () => {
            await clearPendingGenerates();
            refresh();
          }}
          aria-label="clear queue"
        >
          {t("clearQueue")}
        </button>
        <button
          className="bg-gray-200 px-3 py-1 rounded"
          onClick={async () => {
            await clearPendingCollabs();
            refresh();
          }}
          aria-label="clear edits"
        >
          {t("clearEdits")}
        </button>
        <button
          className="bg-gray-200 px-3 py-1 rounded"
          onClick={async () => {
            if (await hasSubscription()) {
              await unsubscribe();
            } else {
              await subscribe();
            }
            setPush(await hasSubscription());
          }}
          aria-label="toggle push"
        >
          {t("togglePush")}
        </button>
        <a
          className="bg-gray-200 px-3 py-1 rounded"
          href="/history"
          download
          aria-label="export history"
        >
          Export History
        </a>
      </div>
      <button className="mt-6 text-blue-600 underline" onClick={onBack} aria-label="back">
        {t("back")}
      </button>
    </main>
  );
}
