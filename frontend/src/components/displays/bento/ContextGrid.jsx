import { useState, Children, cloneElement } from "react";
import "./context-grid.css";

export default function ContextGrid({
  children,
  defaultActive = null,
  allowCollapse = true,
  columns = 2,
}) {
  const [active, setActive] = useState(defaultActive);

  const handleToggle = (index) => {
    if (allowCollapse && active === index) {
      setActive(null);
    } else {
      setActive(index);
    }
  };

  return (
    <div
      className={`context-grid ${
        active !== null ? "has-active" : ""
      } columns-${columns}`}
    >
      {Children.map(children, (child, index) =>
        cloneElement(child, {
          isActive: active === index,
          onToggle: () => handleToggle(index),
          gridIndex: index,
        })
      )}
    </div>
  );
}