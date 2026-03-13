import { useInstance } from "../../context/InstanceContext";

export function SiTiene({ capacidad, children, fallback = null }) {
  const { instance } = useInstance();

  const allowed = instance?.capabilities?.[capacidad];

  if (!allowed) return fallback;

  return children;
}