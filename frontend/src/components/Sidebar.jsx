import { useContext } from "react";
import * as Icons from "react-icons/fa";
import { NavLink } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const SidebarNode = ({ node }) => {
  const Icon = node.icon ? Icons[node.icon] : null;
  const hasChildren = node.content && node.content.length > 0;

  return (
    <li>
      {node.to ? (
        <NavLink to={node.to} className="sidebar-link">
          {Icon && <Icon className="me-2" />}
          {node.label}
        </NavLink>
      ) : (
        <span className="sidebar-group">
          {Icon && <Icon className="me-2" />}
          {node.label}
        </span>
      )}

      {hasChildren && (
        <ul className="list-unstyled ms-3">
          {node.content.map(child => (
            <SidebarNode key={child.key} node={child} />
          ))}
        </ul>
      )}
    </li>
  );
};

export const Sidebar = () => {

  const { menu, isAuthenticated } = useContext(AuthContext);
  if (!(menu && isAuthenticated) )
    return []
  return (
    <nav className="sidebar">
      <ul className="list-unstyled">
        {menu.map(node => (
          <SidebarNode key={node.key} node={node} />
        ))}
      </ul>
    </nav>
  );
};
