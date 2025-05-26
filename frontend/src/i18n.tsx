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
  rating: "Rating",
  back: "Back",
  searchExamples: "Search examples",
  allTags: "All tags",
  favourites: "Favourites",
  allExamples: "All examples",
  cachedResults: "Cached results:",
  queuedRequests: "Queued requests:",
  cachedDetections: "Cached detections:",
  queuedDetections: "Queued detections:",
  clearCache: "Clear Cache",
  clearDetectCache: "Clear Detect Cache",
  clearQueue: "Clear Queue",
  clearDetectQueue: "Clear Detect Queue",
  pendingEdits: "Queued edits:",
  clearEdits: "Clear Edits",
  collabDemo: "Collaboration Demo",
  moderation: "Moderation",
  reports: "Reports",
  clear: "Clear",
  roomId: "Room ID",
  message: "Message",
  send: "Send",
  undo: "Undo",
  redo: "Redo",
  pushEnabled: "Push notifications enabled",
  togglePush: "Toggle Push",
  connectedPeers: "Connected collaborators",
  tutorialTitle: "Welcome to Lego GPT",
  tutorialStep1: "Enter a prompt and optional seed to generate a model.",
  tutorialStep2: "Upload a photo to detect your brick inventory.",
  tutorialStep3: "View and share the generated result.",
  gotIt: "Got it",
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
