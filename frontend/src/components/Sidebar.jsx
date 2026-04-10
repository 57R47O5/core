import "./../styles/sidebar.css"
import { useContext, useState } from "react";
import * as Icons from "react-icons/fa";
import { NavLink } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const SidebarNode = ({ node, onNavigate }) => {
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
            className={({ isActive }) =>
              "sidebar-link" + (isActive ? " active" : "")
            }
            onClick={(e) => {
              if (hasChildren) {
                e.preventDefault();
              } else {
                onNavigate(); // cerrar sidebar al navegar
              }
            }}
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
            <SidebarNode
              key={child.key}
              node={child}
              onNavigate={onNavigate}
            />
          ))}
        </ul>
      )}
    </li>
  );
};

export const Sidebar = ({ isOpen, setIsOpen }) => {
  const { menu, isAuthenticated } = useContext(AuthContext);

  const hayMenu = menu && menu.length > 0;
  if (!hayMenu || !isAuthenticated) return null;

  const toggleSidebar = () => setIsOpen(prev => !prev);
  const closeSidebar = () => setIsOpen(false);

  return (
    <>
      {/* Botón hamburguesa */}
      <button className="sidebar-toggle" onClick={toggleSidebar}>
        ☰
      </button>

      {/* Overlay */}
      {isOpen && <div className="sidebar-overlay" onClick={closeSidebar} />}

      {/* Sidebar */}
      <nav className={`sidebar ${isOpen ? "open" : "collapsed"}`}>
        <ul className="list-unstyled">
          {menu.map(node => (
            <SidebarNode
              key={node.key}
              node={node}
              onNavigate={closeSidebar}
            />
          ))}
        </ul>
      </nav>
    </>
  );
};