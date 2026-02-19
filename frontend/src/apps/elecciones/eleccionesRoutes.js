import campanaRoute from "./routes/campanaRoute";
import colaboradorRoute from "./routes/colaboradorRoute";
import distrito_electoralRoute from "./routes/distrito_electoralRoute";
import lugar_distritoRoute from "./routes/lugar_distritoRoute";
import salidaRoute from "./routes/salidaRoute";
import seccionalRoute from "./routes/seccionalRoute";
import votanteRoute from "./routes/votanteRoute";

const eleccionesRoutes = [
    ...campanaRoute,
    ...colaboradorRoute,
    ...distrito_electoralRoute,
    ...lugar_distritoRoute,
    ...salidaRoute,
    ...seccionalRoute,
    ...votanteRoute,
];

export default eleccionesRoutes;
