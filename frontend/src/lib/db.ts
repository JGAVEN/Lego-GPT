import type { GenerateResponse, DetectResponse } from "../api/lego";

const DB_NAME = "lego-gpt";
const DB_VERSION = 4;
const GEN_STORE = "generate";
const PENDING_STORE = "pending";
const COLLAB_STORE = "pending-collab";
const DETECT_STORE = "detect";
const PENDING_DETECT_STORE = "pending-detect";

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
      if (!db.objectStoreNames.contains(COLLAB_STORE)) {
        db.createObjectStore(COLLAB_STORE, { autoIncrement: true });
      }
      if (!db.objectStoreNames.contains(DETECT_STORE)) {
        db.createObjectStore(DETECT_STORE);
      }
      if (!db.objectStoreNames.contains(PENDING_DETECT_STORE)) {
        db.createObjectStore(PENDING_DETECT_STORE, { autoIncrement: true });
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

export interface PendingDetect {
  image: string;
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
export const countCachedDetects = () => countStore(DETECT_STORE);
export const countPendingDetects = () => countStore(PENDING_DETECT_STORE);

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

export async function getCachedDetect(key: string): Promise<DetectResponse | undefined> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(DETECT_STORE, "readonly");
    const store = tx.objectStore(DETECT_STORE);
    const req = store.get(key);
    req.onsuccess = () => resolve((req.result as DetectResponse | undefined) ?? undefined);
    req.onerror = () => reject(req.error);
  });
}

export async function setCachedDetect(key: string, value: DetectResponse): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(DETECT_STORE, "readwrite");
    const store = tx.objectStore(DETECT_STORE);
    const req = store.put(value, key);
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

export async function addPendingDetect(req: PendingDetect): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(PENDING_DETECT_STORE, "readwrite");
    const store = tx.objectStore(PENDING_DETECT_STORE);
    const r = store.add(req);
    r.onsuccess = () => resolve();
    r.onerror = () => reject(r.error);
  });
}

export async function getPendingDetects(): Promise<Array<{ id: number; request: PendingDetect }>> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(PENDING_DETECT_STORE, "readonly");
    const store = tx.objectStore(PENDING_DETECT_STORE);
    const results: Array<{ id: number; request: PendingDetect }> = [];
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

export async function deletePendingDetect(id: number): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(PENDING_DETECT_STORE, "readwrite");
    const store = tx.objectStore(PENDING_DETECT_STORE);
    const req = store.delete(id);
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

export async function clearCachedDetects(): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(DETECT_STORE, "readwrite");
    const store = tx.objectStore(DETECT_STORE);
    const req = store.clear();
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

export async function clearPendingDetects(): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(PENDING_DETECT_STORE, "readwrite");
    const store = tx.objectStore(PENDING_DETECT_STORE);
    const req = store.clear();
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

export interface PendingCollab {
  room: string;
  data: string;
}

export async function addPendingCollab(msg: PendingCollab): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(COLLAB_STORE, "readwrite");
    const store = tx.objectStore(COLLAB_STORE);
    const r = store.add(msg);
    r.onsuccess = () => resolve();
    r.onerror = () => reject(r.error);
  });
}

export async function getPendingCollabs(): Promise<Array<{ id: number; msg: PendingCollab }>> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(COLLAB_STORE, "readonly");
    const store = tx.objectStore(COLLAB_STORE);
    const results: Array<{ id: number; msg: PendingCollab }> = [];
    const req = store.openCursor();
    req.onsuccess = () => {
      const cursor = req.result;
      if (cursor) {
        results.push({ id: cursor.key as number, msg: cursor.value });
        cursor.continue();
      } else {
        resolve(results);
      }
    };
    req.onerror = () => reject(req.error);
  });
}

export async function deletePendingCollab(id: number): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(COLLAB_STORE, "readwrite");
    const store = tx.objectStore(COLLAB_STORE);
    const req = store.delete(id);
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

export const countPendingCollabs = () => countStore(COLLAB_STORE);

export async function clearPendingCollabs(): Promise<void> {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(COLLAB_STORE, "readwrite");
    const store = tx.objectStore(COLLAB_STORE);
    const req = store.clear();
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}
