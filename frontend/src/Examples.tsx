import { useEffect, useState } from "react";
import { useI18n } from "./i18n";

interface Example {
  id: string;
  title: string;
  prompt: string;
  image: string;
}

export default function Examples({
  onSelect,
  onBack,
}: {
  onSelect: (prompt: string) => void;
  onBack: () => void;
}) {
  const { t } = useI18n();
  const [examples, setExamples] = useState<Example[]>([]);

  useEffect(() => {
    fetch("/examples.json")
      .then((res) => res.json())
      .then((data) => setExamples(data as Example[]))
      .catch(() => setExamples([]));
  }, []);

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">{t("communityExamples")}</h1>
      <div className="space-y-4">
        {examples.map((ex) => (
          <div key={ex.id} className="border p-2 rounded">
            <img src={ex.image} alt={ex.title} className="w-full h-auto mb-2" />
            <h2 className="font-semibold">{ex.title}</h2>
            <p className="text-sm mb-2">{ex.prompt}</p>
            <button
              className="bg-blue-600 text-white px-3 py-1 rounded"
              onClick={() => {
                onSelect(ex.prompt);
                onBack();
              }}
              aria-label="use prompt"
            >
              {t("usePrompt")}
            </button>
          </div>
        ))}
      </div>
      <button className="mt-6 text-blue-600 underline" onClick={onBack} aria-label="back">
        {t("back")}
      </button>
    </main>
  );
}
