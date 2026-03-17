import authRoutes from "../apps/auth/routes/authRoutes";
import baseRoutes from "../apps/base/routes/baseRoutes";
import eleccionesRoutes  from "../apps/elecciones/eleccionesRoutes";
 
export default [
  ...authRoutes,
  ...baseRoutes,
  ...eleccionesRoutes
];
