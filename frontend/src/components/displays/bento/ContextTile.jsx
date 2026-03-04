import { useState } from "react";
import { Card, Badge } from "react-bootstrap";

export default function ContextTile({
  title,
  summary,
  badge,
  icon,
  children,
  canExpand = true,
  defaultExpanded = false,
  isActive: controlledActive,
  onToggle,
  disabled = false,
}) {
  // Permite modo controlado o no controlado
  const [internalActive, setInternalActive] = useState(defaultExpanded);

  const isControlled = controlledActive !== undefined;
  const isActive = isControlled ? controlledActive : internalActive;

  const handleToggle = () => {
    if (disabled || !canExpand) return;

    if (isControlled) {
      onToggle?.(!controlledActive);
    } else {
      setInternalActive((prev) => !prev);
    }
  };

  return (
    <Card
      className={`context-tile 
        ${isActive ? "expanded" : "collapsed"} 
        ${disabled ? "disabled" : ""}
        ${!isActive && summary ? "has-subtitle" : ""}
        ${!isActive && !summary ? "no-subtitle" : ""} 
      `}
      onClick={handleToggle}
      style={{ cursor: canExpand && !disabled ? "pointer" : "default" }}
    >
      <Card.Body>
        {/* HEADER */}
        <div className="d-flex justify-content-between align-items-start">
          <div className="d-flex align-items-center gap-2">
            {icon && <div className="context-icon">{icon}</div>}
            <Card.Title className="mb-0">{title}</Card.Title>
          </div>

          {badge && (
            <Badge bg="secondary" pill>
              {badge}
            </Badge>
          )}
        </div>

        {/* SUMMARY (visible when collapsed) */}
        {!isActive && summary && (
          <div className="context-summary mt-2 text-muted small">
            {summary}
          </div>
        )}

        {/* EXPANDED CONTENT */}
        {isActive && canExpand && (
          <div
            className="context-content mt-3"
            onClick={(e) => e.stopPropagation()} // evita colapsar al interactuar
          >
            {children}
          </div>
        )}
      </Card.Body>
    </Card>
  );
}