import { Card } from "react-bootstrap";
import "./CenteredCard.css";

const CenteredCard = ({
  title,
  subtitle,
  headerActions,
  children,
  maxWidth = "750px",
  className = "",
  bodyClassName = "",
  ...props
}) => {
  return (
    <div className="centered-card-wrapper">
      <Card
        className={`centered-card shadow-sm ${className}`}
        style={{ maxWidth }}
        {...props}
      >
        {(title || headerActions) && (
          <Card.Header className="centered-card-header">
            <div className="centered-card-header-content">
              <div>
                {title && <h5 className="centered-card-title">{title}</h5>}
                {subtitle && (
                  <small className="centered-card-subtitle">
                    {subtitle}
                  </small>
                )}
              </div>
              {headerActions && (
                <div className="centered-card-actions">
                  {headerActions}
                </div>
              )}
            </div>
          </Card.Header>
        )}

        <Card.Body className={`centered-card-body ${bodyClassName}`}>
          {children}
        </Card.Body>
      </Card>
    </div>
  );
};

export default CenteredCard;