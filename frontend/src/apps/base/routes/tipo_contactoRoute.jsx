
import TipoContactoListPage from "../tipo_contacto/TipoContactoListPage";
import TipoContactoFormPage from "../tipo_contacto/TipoContactoFormPage";

const tipo_contactoRoutes = [
    {
        path: "/tipo-contacto",
        element: <TipoContactoListPage />,
    },
    {
        path: "/tipo-contacto/:id",
        element: <TipoContactoFormPage />,
    }
];

export default tipo_contactoRoutes
