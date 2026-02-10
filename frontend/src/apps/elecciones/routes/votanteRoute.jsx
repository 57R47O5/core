
import VotanteListPage from "../votante/VotanteListPage";
import VotanteFormPage from "../votante/VotanteFormPage";

const votanteRoutes = [
    {
        path: "/votante",
        element: <VotanteListPage />,
    },
    {
        path: "/votante/:id",
        element: <VotanteFormPage />,
    }
];

export default votanteRoutes
