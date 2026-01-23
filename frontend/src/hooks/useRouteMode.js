import { useParams } from "react-router-dom";
import { useMemo } from "react";

export function useRouteMode() {
  const { id } = useParams();

  const mode = useMemo(() => {
    if (id === "nuevo") return "create";
    if (id && !isNaN(Number(id))) return "edit";
    if (!id) return "view"; 
    return "unknown";
  }, [id]);

  return {
    id,
    mode,
    isCreate: mode === "create",
    isEdit: mode === "edit",
    isView: mode === "view",
  };
}
