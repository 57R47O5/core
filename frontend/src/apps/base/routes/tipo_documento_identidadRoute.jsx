
import TipoDocumentoIdentidadListPage from "../tipo_documento_identidad/TipoDocumentoIdentidadListPage";
import TipoDocumentoIdentidadFormPage from "../tipo_documento_identidad/TipoDocumentoIdentidadFormPage";

const tipo_documento_identidadRoutes = [
    {
        path: "/tipo-documento-identidad",
        element: <TipoDocumentoIdentidadListPage />,
    },
    {
        path: "/tipo-documento-identidad/:id",
        element: <TipoDocumentoIdentidadFormPage />,
    },
    {
        path: "/tipo-documento-identidad/nuevo",
        element: <TipoDocumentoIdentidadFormPage />,
    }
];

export default tipo_documento_identidadRoutes
