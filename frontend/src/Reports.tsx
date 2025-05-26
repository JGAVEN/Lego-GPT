import { useEffect, useState } from "react";
import { useI18n } from "./i18n";

interface ReportItem {
  id: string;
  count: number;
}

export default function Reports({ onBack }: { onBack: () => void }) {
  const { t } = useI18n();
  const [items, setItems] = useState<ReportItem[]>([]);

  useEffect(() => {
    fetch("/reports")
      .then((res) => res.json())
      .then((d) => setItems(d.reports ?? []))
      .catch(() => setItems([]));
  }, []);

  function clear(id: string) {
    fetch("/reports/clear", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id }),
    }).then(() => setItems((s) => s.filter((x) => x.id !== id)));
  }

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">{t("reports")}</h1>
      <ul className="space-y-2 mb-4">
        {items.map((r) => (
          <li key={r.id} className="border p-2 rounded text-sm">
            {r.id} ({r.count})
            <button
              className="ml-2 text-blue-600 underline"
              onClick={() => clear(r.id)}
            >
              {t("clear")}
            </button>
          </li>
        ))}
      </ul>
      <button className="underline" onClick={onBack} aria-label="back">
        {t("back")}
      </button>
    </main>
  );
}
