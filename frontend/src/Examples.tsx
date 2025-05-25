import { useEffect, useState } from "react";
import { useI18n } from "./i18n";

interface Example {
  id: string;
  title: string;
  prompt: string;
  image: string;
  tags?: string[];
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
  const [search, setSearch] = useState("");
  const [tagFilter, setTagFilter] = useState("");

  useEffect(() => {
    fetch("/examples.json")
      .then((res) => res.json())
      .then((data) => setExamples(data as Example[]))
      .catch(() => setExamples([]));
  }, []);

  const tags = Array.from(
    new Set(examples.flatMap((e) => e.tags ?? []))
  );

  const filtered = examples.filter((ex) => {
    const matchesTag = tagFilter ? ex.tags?.includes(tagFilter) : true;
    const text = `${ex.title} ${ex.prompt}`.toLowerCase();
    const matchesSearch = search
      ? text.includes(search.toLowerCase())
      : true;
    return matchesTag && matchesSearch;
  });

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">{t("communityExamples")}</h1>

      <div className="mb-4 flex gap-2">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder={t("searchExamples")}
          className="flex-1 border rounded px-2 py-1"
          aria-label="search examples"
        />
        {tags.length > 0 && (
          <select
            value={tagFilter}
            onChange={(e) => setTagFilter(e.target.value)}
            className="border rounded px-2 py-1"
            aria-label="filter by tag"
          >
            <option value="">{t("allTags")}</option>
            {tags.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        )}
      </div>

      <div className="space-y-4">
        {filtered.map((ex) => (
          <div key={ex.id} className="border p-2 rounded">
            <img src={ex.image} alt={ex.title} className="w-full h-auto mb-2" />
            <h2 className="font-semibold">{ex.title}</h2>
            <p className="text-sm mb-2">{ex.prompt}</p>
            {ex.tags && (
              <p className="text-xs mb-2">{ex.tags.join(", ")}</p>
            )}
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
      <button
        className="mt-6 text-blue-600 underline"
        onClick={onBack}
        aria-label="back"
      >
        {t("back")}
      </button>
    </main>
  );
}
