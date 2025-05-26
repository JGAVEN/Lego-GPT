import { useState } from "react";
import { useI18n } from "./i18n";

export default function ImportExamples({ onBack }: { onBack: () => void }) {
  const { t } = useI18n();
  const [url, setUrl] = useState("");
  const [status, setStatus] = useState<string | null>(null);

  async function handleImport() {
    if (!url) return;
    try {
      const res = await fetch(url.replace(/\/$/, "") + "/examples.json");
      const data = await res.json();
      const extra = localStorage.getItem("extraExamples");
      const extras = extra ? JSON.parse(extra) : [];
      localStorage.setItem("extraExamples", JSON.stringify([...extras, ...data]));
      setStatus(`Imported ${data.length} examples`);
    } catch (err) {
      setStatus("Failed to import");
    }
  }

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">{t("importExamples")}</h1>
      <input
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="https://example.com"
        className="border rounded px-2 py-1 w-full mb-2"
        aria-label="instance url"
      />
      <button
        onClick={handleImport}
        className="bg-blue-600 text-white px-4 py-2 rounded"
        aria-label="import"
      >
        {t("import")}
      </button>
      {status && <p className="mt-2 text-sm">{status}</p>}
      <button className="mt-6 text-blue-600 underline" onClick={onBack} aria-label="back">
        {t("back")}
      </button>
    </main>
  );
}
