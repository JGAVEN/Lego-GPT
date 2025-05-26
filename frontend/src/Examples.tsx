import { useEffect, useState } from "react";
import { useI18n } from "./i18n";
import { fetchComments, postComment } from "./api/lego";

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
  const [ratings, setRatings] = useState<Record<string, number>>(() => {
    const r = localStorage.getItem("ratings");
    return r ? JSON.parse(r) : {};
  });
  const [favs, setFavs] = useState<string[]>(() => {
    const f = localStorage.getItem("favs");
    return f ? JSON.parse(f) : [];
  });
  const [viewFavs, setViewFavs] = useState(false);

  useEffect(() => {
    fetch("/examples.json")
      .then((res) => res.json())
      .then((data) => {
        const extra = localStorage.getItem("extraExamples");
        const extras = extra ? JSON.parse(extra) : [];
        setExamples([...data, ...extras]);
      })
      .catch(() => {
        const extra = localStorage.getItem("extraExamples");
        const extras = extra ? JSON.parse(extra) : [];
        setExamples(extras);
      });
  }, []);

  const tags = Array.from(
    new Set(examples.flatMap((e) => e.tags ?? []))
  );

  const filtered = examples.filter((ex) => {
    if (viewFavs && !favs.includes(ex.id)) return false;
    const matchesTag = tagFilter ? ex.tags?.includes(tagFilter) : true;
    const text = `${ex.title} ${ex.prompt}`.toLowerCase();
    const matchesSearch = search
      ? text.includes(search.toLowerCase())
      : true;
    return matchesTag && matchesSearch;
  });

  function setRating(id: string, value: number) {
    const next = { ...ratings, [id]: value };
    setRatings(next);
    localStorage.setItem("ratings", JSON.stringify(next));
  }

  function toggleFav(id: string) {
    let next;
    if (favs.includes(id)) {
      next = favs.filter((f) => f !== id);
    } else {
      next = [...favs, id];
    }
    setFavs(next);
    localStorage.setItem("favs", JSON.stringify(next));
  }

  function Comments({ id }: { id: string }) {
    const [list, setList] = useState<{ user: string; text: string }[]>([]);
    const [text, setText] = useState("");

    useEffect(() => {
      fetchComments(id)
        .then((c) => setList(c))
        .catch(() => setList([]));
    }, [id]);

    async function submit() {
      if (!text) return;
      await postComment(id, text);
      setList((l) => [...l, { user: "you", text }]);
      setText("");
    }

    return (
      <div className="mt-2">
        {list.map((c, i) => (
          <p key={i} className="text-xs">
            {c.user}: {c.text}
          </p>
        ))}
        <div className="flex mt-1 gap-1">
          <input
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="border rounded px-1 text-xs flex-1"
            aria-label="comment"
          />
          <button onClick={submit} className="text-xs underline" aria-label="send comment">
            Send
          </button>
        </div>
      </div>
    );
  }

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
        <button
          onClick={() => setViewFavs((v) => !v)}
          className="border rounded px-2 py-1"
          aria-label="toggle favourites"
        >
          {viewFavs ? t("allExamples") : t("favourites")}
        </button>
      </div>

      <div className="space-y-4">
        {filtered.map((ex) => (
          <div key={ex.id} className="border p-2 rounded">
            <img src={ex.image} alt={ex.title} className="w-full h-auto mb-2" />
            <h2 className="font-semibold">{ex.title}</h2>
          <p className="text-sm mb-2">{ex.prompt}</p>
          <div className="mb-2 flex items-center gap-2">
              {[1, 2, 3, 4, 5].map((n) => (
                <button
                  key={n}
                  onClick={() => setRating(ex.id, n)}
                  className={(n <= (ratings[ex.id] ?? 0) ? "text-yellow-500" : "text-gray-300") + " px-2"}
                  aria-label={`rate ${n}`}
                >
                  ★
                </button>
              ))}
              <button onClick={() => toggleFav(ex.id)} aria-label="favourite">
                {favs.includes(ex.id) ? "♥" : "♡"}
              </button>
          </div>
          {ratings[ex.id] && (
            <p className="text-xs mb-1">{t("rating")}: {ratings[ex.id]}/5</p>
          )}
          {ex.tags && (
            <p className="text-xs mb-2">{ex.tags.join(", ")}</p>
          )}
          <button
            onClick={() => {
              if (navigator.share) {
                navigator.share({ title: ex.title, text: ex.prompt, url: location.href });
              } else {
                window.open(
                  `https://twitter.com/intent/tweet?text=${encodeURIComponent(ex.prompt)}`,
                  "_blank"
                );
              }
            }}
            className="text-xs underline mr-2"
            aria-label="share"
          >
            Share
          </button>
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
          <Comments id={ex.id} />
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
