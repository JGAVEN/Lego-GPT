export async function hasPushSupport(): Promise<boolean> {
  return 'serviceWorker' in navigator && 'PushManager' in window;
}

export async function hasSubscription(): Promise<boolean> {
  if (!('serviceWorker' in navigator)) return false;
  const reg = await navigator.serviceWorker.ready;
  const sub = await reg.pushManager.getSubscription();
  return sub !== null;
}

export async function subscribe(): Promise<boolean> {
  if (!(await hasPushSupport())) return false;
  const reg = await navigator.serviceWorker.ready;
  try {
    await reg.pushManager.subscribe({ userVisibleOnly: true });
    return true;
  } catch {
    return false;
  }
}

export async function unsubscribe(): Promise<void> {
  if (!('serviceWorker' in navigator)) return;
  const reg = await navigator.serviceWorker.ready;
  const sub = await reg.pushManager.getSubscription();
  if (sub) await sub.unsubscribe();
}
