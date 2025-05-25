import { createContext, useContext, useState, ReactNode } from "react";

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
  language: "Language:",
  collaboration: "Collaboration",
  send: "Send",
  room: "Room",
  collabEdit: "New edit received",
};

const es: typeof en = {
  title: "Demostración de Lego GPT",
  installApp: "Instalar Aplicación",
  settings: "Configuración",
  examples: "Ejemplos",
  prompt: "Solicitud",
  seedOptional: "Semilla (opcional)",
  inventoryPhoto: "Foto de Inventario",
  detecting: "Detectando…",
  detectedInventory: "Inventario Detectado:",
  generate: "Generar",
  generating: "Generando…",
  viewInAR: "Ver en AR",
  communityExamples: "Ejemplos de la Comunidad",
  usePrompt: "Usar Solicitud",
  back: "Atrás",
  cachedResults: "Resultados en caché:",
  queuedRequests: "Solicitudes en cola:",
  clearCache: "Limpiar Caché",
  clearQueue: "Vaciar Cola",
  language: "Idioma:",
  collaboration: "Colaboración",
  send: "Enviar",
  room: "Sala",
  collabEdit: "Nueva edición recibida",
};

const fr: typeof en = {
  title: "Démo Lego GPT",
  installApp: "Installer l'application",
  settings: "Paramètres",
  examples: "Exemples",
  prompt: "Invite",
  seedOptional: "Graine (optionnel)",
  inventoryPhoto: "Photo d'inventaire",
  detecting: "Détection…",
  detectedInventory: "Inventaire détecté :",
  generate: "Générer",
  generating: "Génération…",
  viewInAR: "Voir en AR",
  communityExamples: "Exemples de la communauté",
  usePrompt: "Utiliser l'invite",
  back: "Retour",
  cachedResults: "Résultats en cache :",
  queuedRequests: "Requêtes en attente :",
  clearCache: "Vider le cache",
  clearQueue: "Vider la file",
  language: "Langue :",
  collaboration: "Collaboration",
  send: "Envoyer",
  room: "Salle",
  collabEdit: "Nouvelle modification reçue",
};

const messages = { en, es, fr };
export type Lang = keyof typeof messages;
export type TransKey = keyof typeof en;

interface I18nContext {
  lang: Lang;
  setLang: (l: Lang) => void;
  t: (k: TransKey) => string;
}

const I18nContext = createContext<I18nContext>({
  lang: "en",
  setLang: () => {},
  t: (k: TransKey) => en[k],
});

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(() => {
    const stored = localStorage.getItem("lang") as Lang | null;
    return stored ?? "en";
  });
  function setLang(l: Lang) {
    setLangState(l);
    localStorage.setItem("lang", l);
  }
  const t = (k: TransKey) => messages[lang][k] ?? en[k];
  return (
    <I18nContext.Provider value={{ lang, setLang, t }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  return useContext(I18nContext);
}
