import campanaRoute from "./routes/campanaRoute";
import ciclo_electoralRoute from "./routes/ciclo_electoralRoute";
import colaboradorRoute from "./routes/colaboradorRoute";
import estado_salidaRoute from "./routes/estado_salidaRoute";
import resultado_visitaRoute from "./routes/resultado_visitaRoute";
import salidaRoute from "./routes/salidaRoute";
import seccionalRoute from "./routes/seccionalRoute";
import votanteRoute from "./routes/votanteRoute";

const eleccionesRoutes = [
    ...campanaRoute,
    ...ciclo_electoralRoute,
    ...colaboradorRoute,
    ...estado_salidaRoute,
    ...resultado_visitaRoute,
    ...salidaRoute,
    ...seccionalRoute,
    ...votanteRoute,
];

export default eleccionesRoutes;
