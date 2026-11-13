import { useCallback, useState } from "react";
export function useLocalStorage<T>(key: string, initial: T) {
  const [value, setValue] = useState<T>(() => {
    try { const raw = localStorage.getItem(key); return raw ? (JSON.parse(raw) as T) : initial; } catch { return initial; }
  });
  const set = useCallback((v: T) => { setValue(v); try { localStorage.setItem(key, JSON.stringify(v)); } catch { /* blocked */ } }, [key]);
  const clear = useCallback(() => { try { localStorage.removeItem(key); } catch { /* ignore */ } }, [key]);
  return [value, set, clear] as const;
}
