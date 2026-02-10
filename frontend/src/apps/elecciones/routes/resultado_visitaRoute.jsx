
import ResultadoVisitaListPage from "../resultado_visita/ResultadoVisitaListPage";
import ResultadoVisitaFormPage from "../resultado_visita/ResultadoVisitaFormPage";

const resultado_visitaRoutes = [
    {
        path: "/resultado-visita",
        element: <ResultadoVisitaListPage />,
    },
    {
        path: "/resultado-visita/:id",
        element: <ResultadoVisitaFormPage />,
    }
];

export default resultado_visitaRoutes
