
import ContactoListPage from "../contacto/ContactoListPage";
import ContactoFormPage from "../contacto/ContactoFormPage";

const contactoRoutes = [
    {
        path: "/contacto",
        element: <ContactoListPage />,
    },
    {
        path: "/contacto/:id",
        element: <ContactoFormPage />,
    }
];

export default contactoRoutes
