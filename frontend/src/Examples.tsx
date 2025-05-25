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
  const [custom, setCustom] = useState<Example[]>([]);
  const [title, setTitle] = useState("");
  const [promptText, setPromptText] = useState("");
  const [image, setImage] = useState("");

  useEffect(() => {
    fetch("/examples.json")
      .then((res) => res.json())
      .then((data) => setExamples(data as Example[]))
      .catch(() => setExamples([]));
    const stored = localStorage.getItem("custom-examples");
    if (stored) {
      try {
        setCustom(JSON.parse(stored) as Example[]);
      } catch {
        setCustom([]);
      }
    }
  }, []);

  function addExample() {
    const ex: Example = {
      id: Date.now().toString(),
      title,
      prompt: promptText,
      image,
    };
    const next = [...custom, ex];
    setCustom(next);
    localStorage.setItem("custom-examples", JSON.stringify(next));
    setTitle("");
    setPromptText("");
    setImage("");
  }

  const allExamples = [...examples, ...custom];

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">{t("communityExamples")}</h1>
      <div className="space-y-4">
        {allExamples.map((ex) => (
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
      <form
        className="mt-4 space-y-2"
        onSubmit={(e) => {
          e.preventDefault();
          addExample();
        }}
      >
        <h2 className="font-semibold">{t("addExample")}</h2>
        <input
          className="border rounded w-full px-2 py-1"
          placeholder={t("exampleTitle")}
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <input
          className="border rounded w-full px-2 py-1"
          placeholder={t("examplePrompt")}
          value={promptText}
          onChange={(e) => setPromptText(e.target.value)}
          required
        />
        <input
          className="border rounded w-full px-2 py-1"
          placeholder={t("exampleImage")}
          value={image}
          onChange={(e) => setImage(e.target.value)}
        />
        <button className="bg-blue-600 text-white px-3 py-1 rounded" type="submit">
          {t("addExample")}
        </button>
      </form>
      <button className="mt-6 text-blue-600 underline" onClick={onBack} aria-label="back">
        {t("back")}
      </button>
    </main>
  );
}
