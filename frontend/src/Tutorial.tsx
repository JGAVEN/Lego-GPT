import { useI18n } from "./i18n";

export default function Tutorial({ onClose }: { onClose: () => void }) {
  const { t } = useI18n();
  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 text-white p-4 flex flex-col items-center justify-center z-50">
      <h2 className="text-xl font-bold mb-4">{t("tutorialTitle")}</h2>
      <ol className="list-decimal list-inside text-left max-w-sm mb-4 space-y-2">
        <li>{t("tutorialStep1")}</li>
        <li>{t("tutorialStep2")}</li>
        <li>{t("tutorialStep3")}</li>
      </ol>
      <button onClick={onClose} className="bg-blue-600 px-3 py-1 rounded" aria-label="close tutorial">
        {t("gotIt")}
      </button>
    </div>
  );
}
