import "./../styles/sidebar.css"
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
        onClick={toggle}
        style={{ cursor: hasChildren ? "pointer" : "default" }}
      >
        {node.to ? (
          <NavLink
            to={node.to}
            className="sidebar-link"
            onClick={e => hasChildren && e.preventDefault()}
          >
          <span className="sidebar-group">
          {Icon && (
            <span className="sidebar-icon">
              <Icon />
                </span>
              )}
              <span className="sidebar-label">
                {node.label}
              </span>
            </span>
          </NavLink>
        ) : (
          <span className="sidebar-group">
          {Icon && (
            <span className="sidebar-icon">
              <Icon />
                </span>
              )}
              <span className="sidebar-label">
                {node.label}
              </span>
            </span>
        )}        
      </div>
      {hasChildren && open && (
        <ul className="sidebar-submenu">
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

