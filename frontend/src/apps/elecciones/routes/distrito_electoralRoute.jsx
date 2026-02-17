
import DistritoElectoralListPage from "../distrito_electoral/DistritoElectoralListPage";
import DistritoElectoralFormPage from "../distrito_electoral/DistritoElectoralFormPage";

const distrito_electoralRoutes = [
    {
        path: "/distrito-electoral",
        element: <DistritoElectoralListPage />,
    },
    {
        path: "/distrito-electoral/:id",
        element: <DistritoElectoralFormPage />,
    }
];

export default distrito_electoralRoutes
