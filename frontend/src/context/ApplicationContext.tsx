import { createContext, useContext, type ReactNode } from "react";
import type { ApplicationState } from "../types";
import { useApplicationStore, type Action } from "../store/useApplicationStore";

const Ctx = createContext<{ state: ApplicationState; dispatch: (action: Action) => void } | null>(null);
export function ApplicationProvider({ children }: { children: ReactNode }) {
  const state = useApplicationStore();
  return <Ctx.Provider value={{ state, dispatch: state.dispatch }}>{children}</Ctx.Provider>;
}
export function useApplication() {
  const context = useContext(Ctx);
  if (!context) throw new Error("Missing ApplicationProvider");
  return context;
}
