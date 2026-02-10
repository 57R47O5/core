
import EstadoSalidaListPage from "../estado_salida/EstadoSalidaListPage";
import EstadoSalidaFormPage from "../estado_salida/EstadoSalidaFormPage";

const estado_salidaRoutes = [
    {
        path: "/estado-salida",
        element: <EstadoSalidaListPage />,
    },
    {
        path: "/estado-salida/:id",
        element: <EstadoSalidaFormPage />,
    }
];

export default estado_salidaRoutes
