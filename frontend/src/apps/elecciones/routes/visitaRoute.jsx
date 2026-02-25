
import VisitaListPage from "../visita/VisitaListPage";
import VisitaFormPage from "../visita/VisitaFormPage";

const visitaRoutes = [
    {
        path: "/visita",
        element: <VisitaListPage />,
    },
    {
        path: "/visita/:id",
        element: <VisitaFormPage />,
    }
];

export default visitaRoutes
