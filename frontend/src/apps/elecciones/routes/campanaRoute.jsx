
import CampanaListPage from "../campana/CampanaListPage";
import CampanaFormPage from "../campana/CampanaFormPage";

const campanaRoutes = [
    {
        path: "/campana",
        element: <CampanaListPage />,
    },
    {
        path: "/campana/:id",
        element: <CampanaFormPage />,
    }
];

export default campanaRoutes
