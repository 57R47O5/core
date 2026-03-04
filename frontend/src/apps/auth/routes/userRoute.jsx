
import UserListPage from "../user/UserListPage";
import UserFormPage from "../user/UserFormPage";

const userRoutes = [
    {
        path: "/user",
        element: <UserListPage />,
    },
    {
        path: "/user/:id",
        element: <UserFormPage />,
    },
    {
        path: "/user/nuevo",
        element: <UserFormPage />,
    }
];

export default userRoutes