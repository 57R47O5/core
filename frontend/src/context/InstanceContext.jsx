import { useModelInstance } from "../hooks/useModelInstance";
import { createContext, useContext } from "react";

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

  const value = {
    instance,
    loading,
    exists,
  };

  return (
    <InstanceContext.Provider value={value}>
      {children}
    </InstanceContext.Provider>
  );
}
