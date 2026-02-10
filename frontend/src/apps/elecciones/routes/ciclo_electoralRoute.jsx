
import CicloElectoralListPage from "../ciclo_electoral/CicloElectoralListPage";
import CicloElectoralFormPage from "../ciclo_electoral/CicloElectoralFormPage";

const ciclo_electoralRoutes = [
    {
        path: "/ciclo-electoral",
        element: <CicloElectoralListPage />,
    },
    {
        path: "/ciclo-electoral/:id",
        element: <CicloElectoralFormPage />,
    }
];

export default ciclo_electoralRoutes
