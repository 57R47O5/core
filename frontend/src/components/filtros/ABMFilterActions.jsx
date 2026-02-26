import { Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const ABMFilterActions = ({
  controller,
  loading,
  showNew = true,
  newLabel = "Nuevo"
}) => {
  const navigate = useNavigate();

  return (
    <div className="text-end d-flex gap-2 justify-content-end">
      <Button type="submit" variant="primary" disabled={loading}>
        Buscar
      </Button>

      {showNew && (
        <Button
          variant="secondary"
          disabled={loading}
          onClick={() => navigate(`/${controller}/nuevo`)}
        >
          {newLabel}
        </Button>
      )}
    </div>
  );
};

export default ABMFilterActions;