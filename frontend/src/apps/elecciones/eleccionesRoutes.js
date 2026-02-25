import campanaRoute from "./routes/campanaRoute";
import ciclo_electoralRoutes from "./routes/ciclo_electoralRoute";
import colaboradorRoute from "./routes/colaboradorRoute";
import distrito_electoralRoute from "./routes/distrito_electoralRoute";
import lugar_distritoRoute from "./routes/lugar_distritoRoute";
import salidaRoute from "./routes/salidaRoute";
import seccionalRoute from "./routes/seccionalRoute";
import visitaRoute from "./routes/visitaRoute";
import votanteRoute from "./routes/votanteRoute";

const eleccionesRoutes = [
    ...campanaRoute,
    ...ciclo_electoralRoutes,
    ...colaboradorRoute,
    ...distrito_electoralRoute,
    ...lugar_distritoRoute,
    ...salidaRoute,
    ...seccionalRoute,
    ...visitaRoute,
    ...votanteRoute,
];

export default eleccionesRoutes;
