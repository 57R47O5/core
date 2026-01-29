import { Card } from "react-bootstrap";
import CenteredCard from "../displays/CenteredCard";

export function BaseListLayout({ title, FilterComponent, onSearch, loading, children }) {
  return (
    <div className="container">
      <h2 className="mb-4">{title}</h2>

      <CenteredCard>
        <Card.Body>
          <FilterComponent onSearch={onSearch} loading={loading} />
        </Card.Body>
      </CenteredCard>

      <CenteredCard>
        <Card.Body>{children}</Card.Body>
      </CenteredCard>
    </div>
  );
}
