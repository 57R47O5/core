import campanaRoute from "./routes/campanaRoute";
import colaboradorRoute from "./routes/colaboradorRoute";
import salidaRoute from "./routes/salidaRoute";
import seccionalRoute from "./routes/seccionalRoute";
import votanteRoute from "./routes/votanteRoute";

const eleccionesRoutes = [
    ...campanaRoute,
    ...colaboradorRoute,
    ...salidaRoute,
    ...seccionalRoute,
    ...votanteRoute,
];

export default eleccionesRoutes;
