
import ColaboradorListPage from "../colaborador/ColaboradorListPage";
import ColaboradorFormPage from "../colaborador/ColaboradorFormPage";

const colaboradorRoutes = [
    {
        path: "/colaborador",
        element: <ColaboradorListPage />,
    },
    {
        path: "/colaborador/:id",
        element: <ColaboradorFormPage />,
    }
];

export default colaboradorRoutes
