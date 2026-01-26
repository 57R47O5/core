import monedaRoutes from "./monedaRoute";
import personaRoutes from "./personaRoute";
import persona_fisicaRoutes from "./persona_fisicaRoute";
import persona_juridicaRoutes from "./persona_juridicaRoute";
import tipo_documento_identidadRoutes from  "./tipo_documento_identidadRoute";
import documento_identidadRoutes from  "./documento_identidadRoute";

const baseRoutes = [
    ...monedaRoutes,
    ...personaRoutes,
    ...persona_fisicaRoutes,
    ...persona_juridicaRoutes,
    ...tipo_documento_identidadRoutes,
    ...documento_identidadRoutes
]

export default  baseRoutes