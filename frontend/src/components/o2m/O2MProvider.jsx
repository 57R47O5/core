import { createContext, useContext } from "react";
import getAPIBase from "../../api/BaseAPI";

/* =========================
   Context
========================= */

const O2MContext = createContext(null);

export function useO2M() {
  const ctx = useContext(O2MContext);
  if (!ctx) {
    throw new Error("useO2M debe usarse dentro de <O2MProvider>");
  }
  return ctx;
}

/* =========================
   Provider
========================= */

export default function O2MProvider({
  controller,
  columns,
  initialItem,
  validationSchema,
  children,
}) {
  const api = getAPIBase(controller);

  const value = {
    controller,
    columns,
    initialItem,
    validationSchema,
    ...api,
  };

  return (
    <O2MContext.Provider value={value}>
      {children}
    </O2MContext.Provider>
  );
}
