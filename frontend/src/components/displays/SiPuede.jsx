import { useInstance } from "../../context/InstanceContext";

export function SiPuede({ capability, children, fallback = null }) {
  const { instance } = useInstance();

  const allowed = instance?.capabilities?.[capability];

  if (!allowed) return fallback;

  return children;
}