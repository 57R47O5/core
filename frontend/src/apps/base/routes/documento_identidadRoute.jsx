
import DocumentoIdentidadListPage from "../documento_identidad/DocumentoIdentidadListPage";
import DocumentoIdentidadFormPage from "../documento_identidad/DocumentoIdentidadFormPage";

const documento_identidadRoutes = [
    {
        path: "/documento-identidad",
        element: <DocumentoIdentidadListPage />,
    },
    {
        path: "/documento-identidad/:id",
        element: <DocumentoIdentidadFormPage />,
    },
    {
        path: "/documento-identidad/nuevo",
        element: <DocumentoIdentidadFormPage />,
    }
];

export default documento_identidadRoutes
