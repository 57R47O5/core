import { useModelInstance } from "../hooks/useModelInstance";
import { createContext, useContext, useMemo } from "react";

export const InstanceContext = createContext(null);

export function useInstance() {
  const ctx = useContext(InstanceContext);
  if (!ctx) {
    throw new Error("useInstance debe usarse dentro de <InstanceProvider>");
  }
  return ctx;
}

export function InstanceProvider({ controller, id, defaults, children }) {
  const { instance, loading, exists } = useModelInstance({
    controller,
    id,
    defaults,
  });

  const capabilities = instance?.capabilities || {};

  const value = useMemo(() => ({
    instance,
    loading,
    exists,

    capabilities,

    has: (cap) => Boolean(capabilities?.[cap]),

    hasAny: (caps = []) =>
      caps.some((c) => Boolean(capabilities?.[c])),

    hasAll: (caps = []) =>
      caps.every((c) => Boolean(capabilities?.[c])),

  }), [instance, loading, exists]);

  return (
    <InstanceContext.Provider value={value}>
      {children}
    </InstanceContext.Provider>
  );
}