import argparse
import json
import os
from pathlib import Path
from urllib import request


def _translate(text: str, lang: str, url: str) -> str:
    data = json.dumps({"text": text, "target": lang}).encode()
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with request.urlopen(req) as resp:
        out = json.load(resp)
    return out.get("translated", text)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Translate example prompts")
    parser.add_argument("lang", help="Target language code")
    parser.add_argument("--url", default=os.getenv("TRANSLATE_API"), help="Translation API URL")
    parser.add_argument(
        "--examples",
        default=str(Path(__file__).resolve().parents[1] / "frontend/public/examples.json"),
        help="Path to examples.json",
    )
    parser.add_argument("--out", help="Output file")
    args = parser.parse_args(argv)
    if not args.url:
        parser.error("Translation API URL required")
    path = Path(args.examples)
    data = json.loads(path.read_text()) if path.is_file() else []
    translated = []
    for ex in data:
        ex = ex.copy()
        ex["prompt"] = _translate(ex.get("prompt", ""), args.lang, args.url)
        ex["title"] = _translate(ex.get("title", ""), args.lang, args.url)
        translated.append(ex)
    out_path = Path(args.out or f"examples_{args.lang}.json")
    out_path.write_text(json.dumps(translated, indent=2))


if __name__ == "__main__":  # pragma: no cover
    main()
