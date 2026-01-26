
import PersonaListPage from "../persona/PersonaListPage";
import PersonaFormPage from "../persona/PersonaFormPage";

const personaRoutes = [
    {
        path: "/persona",
        element: <PersonaListPage />,
    },
    {
        path: "/persona/:id",
        element: <PersonaFormPage />,
    }
];

export default personaRoutes
