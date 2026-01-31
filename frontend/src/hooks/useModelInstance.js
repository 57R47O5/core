import { useState, useEffect } from "react";
import getAPIBase from "../api/BaseAPI";

export function useModelInstance({ controller, id, defaults }) {
  const [instance, setInstance] = useState(null);
  const [loading, setLoading] = useState(true);

  const {obtener} = getAPIBase(controller);
  const exists = Boolean(id);

  useEffect(() => {
    let mounted = true;

    async function load() {
    setLoading(true);

    if (!exists) {
        setInstance({ ...defaults });
        setLoading(false);
        return;
    }

    try {
        const data = await obtener(id);
        setInstance({ ...defaults, ...data });
    } catch (err) {
        console.error("Error en load:", err);
    } finally {
        setLoading(false);
    }
    }

    load();

    return () => {
      mounted = false;
    };
  }, [controller, id]);

  return {
    instance,
    exists,
    loading,
    reload: () => obtener(controller, id).then(setInstance),
  };
}
