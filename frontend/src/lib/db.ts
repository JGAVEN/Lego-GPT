const DB_NAME = 'lego-gpt';
const DB_VERSION = 1;
const GEN_STORE = 'generate';

function openDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(GEN_STORE)) {
        db.createObjectStore(GEN_STORE);
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export async function getCachedGenerate(key: string) {
  const db = await openDb();
  return new Promise<any>((resolve, reject) => {
    const tx = db.transaction(GEN_STORE, 'readonly');
    const store = tx.objectStore(GEN_STORE);
    const req = store.get(key);
    req.onsuccess = () => resolve(req.result ?? undefined);
    req.onerror = () => reject(req.error);
  });
}

export async function setCachedGenerate(key: string, value: any) {
  const db = await openDb();
  return new Promise<void>((resolve, reject) => {
    const tx = db.transaction(GEN_STORE, 'readwrite');
    const store = tx.objectStore(GEN_STORE);
    const req = store.put(value, key);
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}
