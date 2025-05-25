import { useEffect, useState } from "react";
import { useI18n } from "./i18n";
import { isAdmin } from "./api/lego";

interface Submission {
  file: string;
  title: string;
  prompt: string;
}

export default function Moderation({ onBack }: { onBack: () => void }) {
  const { t } = useI18n();
  const [subs, setSubs] = useState<Submission[]>([]);
  const admin = isAdmin();

  useEffect(() => {
    if (!admin) return;
    fetch("/submissions")
      .then((res) => res.json())
      .then((data) => setSubs(data.submissions ?? []))
      .catch(() => setSubs([]));
  }, [admin]);

  if (!admin) {
    return (
      <main className="p-6 max-w-xl mx-auto font-sans">
        <p>Admin only</p>
        <button className="underline" onClick={onBack} aria-label="back">
          {t("back")}
        </button>
      </main>
    );
  }

  function act(path: string, file: string) {
    fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ file }),
    }).then(() => setSubs((s) => s.filter((x) => x.file !== file)));
  }

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">{t("moderation")}</h1>
      <ul className="space-y-2 mb-4">
        {subs.map((s) => (
          <li key={s.file} className="border p-2 rounded">
            <p className="font-semibold">{s.title}</p>
            <p className="text-sm mb-2">{s.prompt}</p>
            <button
              className="bg-green-600 text-white px-3 py-1 mr-2 rounded"
              onClick={() => act("/submissions/approve", s.file)}
            >
              Approve
            </button>
            <button
              className="bg-red-600 text-white px-3 py-1 rounded"
              onClick={() => act("/submissions/reject", s.file)}
            >
              Reject
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
