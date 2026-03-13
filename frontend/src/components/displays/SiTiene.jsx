import { useInstance } from "../../context/InstanceContext";

export function SiTiene({ capacidad, children, fallback = null }) {
  const { has } = useInstance();

  if (!has(capacidad)) return fallback;

  return children;
}