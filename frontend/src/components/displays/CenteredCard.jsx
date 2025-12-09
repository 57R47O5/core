import React from "react";
import { Card } from "react-bootstrap";

const CenteredCard = ({ children, maxWidth = "750px", className = "", ...props }) => {
  return (
    <div
      className="d-flex justify-content-center px-3 py-3"
      style={{ width: "100%" }}
    >
      <Card
        className={`shadow-sm ${className}`}
        style={{
          width: "100%",
          maxWidth: maxWidth,
          borderRadius: "12px",
        }}
        {...props}
      >
        <Card.Body>{children}</Card.Body>
      </Card>
    </div>
  );
};

export default CenteredCard;
