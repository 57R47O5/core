import { Link } from "react-router-dom";
import "./link.css";

export default function BaseLink({
  to,
  children,
  variant = "default",
  className = "",
}) {
  return (
    <Link
      to={to}
      className={`app-link app-link-${variant} ${className}`}
    >
      {children}
    </Link>
  );
}