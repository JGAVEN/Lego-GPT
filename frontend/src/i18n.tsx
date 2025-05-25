import { createContext, useContext, ReactNode } from "react";

const en = {
  title: "Lego GPT Demo",
  installApp: "Install App",
  settings: "Settings",
  examples: "Examples",
  prompt: "Prompt",
  seedOptional: "Seed (optional)",
  inventoryPhoto: "Inventory Photo",
  detecting: "Detecting…",
  detectedInventory: "Detected Inventory:",
  generate: "Generate",
  generating: "Generating…",
  viewInAR: "View in AR",
  communityExamples: "Community Examples",
  usePrompt: "Use Prompt",
  back: "Back",
  cachedResults: "Cached results:",
  queuedRequests: "Queued requests:",
  clearCache: "Clear Cache",
  clearQueue: "Clear Queue",
}; 

export type Lang = "en";
export type TransKey = keyof typeof en;

interface I18nContext {
  t: (k: TransKey) => string;
}

const I18nContext = createContext<I18nContext>({
  t: (k: TransKey) => en[k],
});

export function I18nProvider({ children }: { children: ReactNode }) {
  const t = (k: TransKey) => en[k];
  return (
    <I18nContext.Provider value={{ t }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  return useContext(I18nContext);
}
