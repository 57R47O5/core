
import PersonaJuridicaListPage from "../persona_juridica/PersonaJuridicaListPage";
import PersonaJuridicaFormPage from "../persona_juridica/PersonaJuridicaFormPage";

const persona_juridicaRoutes = [
    {
        path: "/persona-juridica",
        element: <PersonaJuridicaListPage />,
    },
    {
        path: "/persona-juridica/:id",
        element: <PersonaJuridicaFormPage />,
    }
];

export default persona_juridicaRoutes
