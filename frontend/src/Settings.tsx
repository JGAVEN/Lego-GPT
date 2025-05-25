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

export default function Settings({ onBack }: { onBack: () => void }) {
  const { t } = useI18n();
  const [cacheCount, setCacheCount] = useState(0);
  const [queueCount, setQueueCount] = useState(0);
  const [editCount, setEditCount] = useState(0);
  const [pushEnabled, setPushEnabled] = useState(false);
  const pushSupported = 'serviceWorker' in navigator && 'PushManager' in window;

  async function refresh() {
    setCacheCount(await countCachedGenerates());
    setQueueCount(await countPendingGenerates());
    setEditCount(await countPendingCollabs());
    if (pushSupported) {
      const reg = await navigator.serviceWorker.ready;
      const sub = await reg.pushManager.getSubscription();
      setPushEnabled(!!sub);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function togglePush() {
    if (!pushSupported) return;
    const reg = await navigator.serviceWorker.ready;
    const sub = await reg.pushManager.getSubscription();
    if (sub) {
      await sub.unsubscribe();
      setPushEnabled(false);
    } else {
      try {
        await reg.pushManager.subscribe({ userVisibleOnly: true });
        setPushEnabled(true);
      } catch {
        /* ignore */
      }
    }
  }

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">{t("settings")}</h1>
      <p>{t("cachedResults")} {cacheCount}</p>
      <p>{t("queuedRequests")} {queueCount}</p>
      <p>{t("pendingEdits")} {editCount}</p>
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
        {pushSupported && (
          <button
            className="bg-gray-200 px-3 py-1 rounded"
            onClick={togglePush}
            aria-label="toggle push"
          >
            {t("togglePush")}
          </button>
        )}
      </div>
      {pushSupported && (
        <p className="mt-2 text-sm">
          {t("pushEnabled")}: {pushEnabled ? "yes" : "no"}
        </p>
      )}
      <button className="mt-6 text-blue-600 underline" onClick={onBack} aria-label="back">
        {t("back")}
      </button>
    </main>
  );
}
