
import PersonaFisicaListPage from "../persona_fisica/PersonaFisicaListPage";
import PersonaFisicaFormPage from "../persona_fisica/PersonaFisicaFormPage";

const persona_fisicaRoutes = [
    {
        path: "/persona-fisica",
        element: <PersonaFisicaListPage />,
    },
    {
        path: "/persona-fisica/:id",
        element: <PersonaFisicaFormPage />,
    }
];

export default persona_fisicaRoutes
