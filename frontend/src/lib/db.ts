import type { GenerateResponse } from "../api/lego";

const DB_NAME = "lego-gpt";
const DB_VERSION = 2;
const GEN_STORE = "generate";
const PENDING_STORE = "pending";

function openDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(GEN_STORE)) {
        db.createObjectStore(GEN_STORE);
      }
      if (!db.objectStoreNames.contains(PENDING_STORE)) {
        db.createObjectStore(PENDING_STORE, { autoIncrement: true });
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export async function getCachedGenerate(
  key: string
): Promise<GenerateResponse | undefined> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(GEN_STORE, "readonly");
    const store = tx.objectStore(GEN_STORE);
    const req = store.get(key);
    req.onsuccess = () =>
      resolve((req.result as GenerateResponse | undefined) ?? undefined);
    req.onerror = () => reject(req.error);
  });
}

export async function setCachedGenerate(
  key: string,
  value: GenerateResponse
): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(GEN_STORE, "readwrite");
    const store = tx.objectStore(GEN_STORE);
    const req = store.put(value, key);
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

export interface PendingRequest {
  prompt: string;
  seed: number | null;
  inventory_filter: Record<string, number> | null;
}

export async function addPendingGenerate(req: PendingRequest): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(PENDING_STORE, "readwrite");
    const store = tx.objectStore(PENDING_STORE);
    const r = store.add(req);
    r.onsuccess = () => resolve();
    r.onerror = () => reject(r.error);
  });
}

export async function getPendingGenerates(): Promise<
  Array<{ id: number; request: PendingRequest }>
> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(PENDING_STORE, "readonly");
    const store = tx.objectStore(PENDING_STORE);
    const results: Array<{ id: number; request: PendingRequest }> = [];
    const req = store.openCursor();
    req.onsuccess = () => {
      const cursor = req.result;
      if (cursor) {
        results.push({ id: cursor.key as number, request: cursor.value });
        cursor.continue();
      } else {
        resolve(results);
      }
    };
    req.onerror = () => reject(req.error);
  });
}

export async function deletePendingGenerate(id: number): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(PENDING_STORE, "readwrite");
    const store = tx.objectStore(PENDING_STORE);
    const req = store.delete(id);
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

async function countStore(name: string): Promise<number> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(name, "readonly");
    const store = tx.objectStore(name);
    const req = store.count();
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export const countCachedGenerates = () => countStore(GEN_STORE);
export const countPendingGenerates = () => countStore(PENDING_STORE);

export async function clearCachedGenerates(): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(GEN_STORE, "readwrite");
    const store = tx.objectStore(GEN_STORE);
    const req = store.clear();
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

export async function clearPendingGenerates(): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(PENDING_STORE, "readwrite");
    const store = tx.objectStore(PENDING_STORE);
    const req = store.clear();
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}
