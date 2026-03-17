import { useState, Children, cloneElement } from "react";
import { Spinner, Alert } from "react-bootstrap";
import { InstanceProvider, useInstance } from "../../../context/InstanceContext";
import { useRouteMode } from "../../../hooks/useRouteMode";
import "./context-grid.css";

function ContextGridInner({
  children,
  defaultActive = null,
  allowCollapse = true,
  columns = 2,
}) {
  const { id, loading, exists, instance } = useInstance();
  const [activeKey, setActiveKey] = useState(defaultActive);

  const handleToggle = (key) => {
    if (allowCollapse && activeKey === key) {
      setActiveKey(null);
    } else {
      setActiveKey(key);
    }
  };

  if (loading) {
    return (
      <div className="context-grid-loading text-center p-4">
        <Spinner animation="border" />
      </div>
    );
  }

  return (
    <div
      className={`context-grid ${
        activeKey !== null ? "has-active" : ""
      } columns-${columns}`}
    >
      {Children.map(children, (child) => {
        const key = child.props.tileKey;

        if (!key) {
          throw new Error(
            "Cada ContextTile debe tener una prop 'tileKey' única."
          );
        }

        return cloneElement(child, {
          isActive: key === activeKey,
          onToggle: () => handleToggle(key),
          instance, // opcional, por si algún tile lo quiere
        });
      })}
    </div>
  );
}

export default function ContextGrid({
  controller,
  children,
  defaultActive = null,
  allowCollapse = true,
  columns = 2,
  defaults,
}) {
  const { id } = useRouteMode();

  return (
    <InstanceProvider
      controller={controller}
      id={id}
      defaults={defaults}
    >
      <ContextGridInner
        defaultActive={defaultActive}
        allowCollapse={allowCollapse}
        columns={columns}
      >
        {children}
      </ContextGridInner>
    </InstanceProvider>
  );
}
