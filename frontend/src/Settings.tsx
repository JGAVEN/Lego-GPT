import { useEffect, useState } from "react";
import { useI18n } from "./i18n";
import {
  countCachedGenerates,
  countPendingGenerates,
  clearCachedGenerates,
  clearPendingGenerates,
} from "./lib/db";

export default function Settings({ onBack }: { onBack: () => void }) {
  const { t, lang, setLang } = useI18n();
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
      <h1 className="text-2xl font-bold mb-4">{t("settings")}</h1>
      <div className="mb-4">
        <label className="mr-2">{t("language")}</label>
        <select
          className="border rounded px-2 py-1"
          value={lang}
          onChange={(e) => setLang(e.target.value as typeof lang)}
        >
          <option value="en">English</option>
          <option value="es">Español</option>
        </select>
      </div>
      <p>{t("cachedResults")} {cacheCount}</p>
      <p>{t("queuedRequests")} {queueCount}</p>
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
      </div>
      <button className="mt-6 text-blue-600 underline" onClick={onBack} aria-label="back">
        {t("back")}
      </button>
    </main>
  );
}
