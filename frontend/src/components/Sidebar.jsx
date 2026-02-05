import { useContext, useState } from "react";
import * as Icons from "react-icons/fa";
import { NavLink } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const SidebarNode = ({ node }) => {
  const Icon = node.icon ? Icons[node.icon] : null;
  const hasChildren = node.content && node.content.length > 0;

  const [open, setOpen] = useState(false);

  const toggle = () => {
    if (hasChildren) {
      setOpen(prev => !prev);
    }
  };

  return (
    <li>
      <div
        className="sidebar-item d-flex align-items-center justify-content-between"
        onClick={toggle}
        style={{ cursor: hasChildren ? "pointer" : "default" }}
      >
        {node.to ? (
          <NavLink
            to={node.to}
            className="sidebar-link flex-grow-1"
            onClick={e => hasChildren && e.preventDefault()}
          >
            {Icon && <Icon className="me-2" />}
            {node.label}
          </NavLink>
        ) : (
          <span className="sidebar-group flex-grow-1">
            {Icon && <Icon className="me-2" />}
            {node.label}
          </span>
        )}

        {hasChildren && (
          <span className="ms-2">
            {open ? "▾" : "▸"}
          </span>
        )}
      </div>

      {hasChildren && open && (
        <ul className="list-unstyled ms-3 mt-1">
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

  if (!menu || !isAuthenticated) return null;

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

