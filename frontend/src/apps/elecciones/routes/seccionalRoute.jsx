
import SeccionalListPage from "../seccional/SeccionalListPage";
import SeccionalFormPage from "../seccional/SeccionalFormPage";

const seccionalRoutes = [
    {
        path: "/seccional",
        element: <SeccionalListPage />,
    },
    {
        path: "/seccional/:id",
        element: <SeccionalFormPage />,
    }
];

export default seccionalRoutes
