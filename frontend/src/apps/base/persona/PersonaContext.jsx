import { createContext, useContext } from "react";

const PersonaContext = createContext(null);

export function usePersona() {
  const ctx = useContext(PersonaContext);
  if (!ctx) {
    throw new Error("usePersona must be used inside PersonaProvider");
  }
  return ctx;
}

export function PersonaProvider({ personaId, children }) {
  const value = {
    personaId,
    isResolved: Boolean(personaId),
  };

  return (
    <PersonaContext.Provider value={value}>
      {children}
    </PersonaContext.Provider>
  );
}
