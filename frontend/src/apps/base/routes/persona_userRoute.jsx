
import PersonaUserListPage from "../persona_user/PersonaUserListPage";
import PersonaUserFormPage from "../persona_user/PersonaUserFormPage";

const persona_userRoutes = [
    {
        path: "/persona-user",
        element: <PersonaUserListPage />,
    },
    {
        path: "/persona-user/:id",
        element: <PersonaUserFormPage />,
    },
    {
        path: "/persona-user/nuevo",
        element: <PersonaUserFormPage />,
    }
];

export default persona_userRoutes
