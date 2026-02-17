
import LugarDistritoListPage from "../lugar_distrito/LugarDistritoListPage";
import LugarDistritoFormPage from "../lugar_distrito/LugarDistritoFormPage";

const lugar_distritoRoutes = [
    {
        path: "/lugar-distrito",
        element: <LugarDistritoListPage />,
    },
    {
        path: "/lugar-distrito/:id",
        element: <LugarDistritoFormPage />,
    }
];

export default lugar_distritoRoutes
