import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext"; // ajusta la ruta según tu estructura
import { Button } from "react-bootstrap"; 
import "../App.css";

const Home = () => {
    const { user, isAuthenticated } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleCrearCartel = () => {
        navigate("/carteles/nuevo"); // esta ruta debe apuntar a CrearCartelPage
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-[70vh] text-center gap-4">
            <h1 className="text-3xl font-bold">Bienvenido a la Cartelpy</h1>

            {isAuthenticated ? (
                <>
                    <p className="text-lg text-gray-700">
                        ¡Hola, {user?.username}! 👋
                    </p>
                    <Button
                        onClick={handleCrearCartel}
                        className="mt-4 px-6 py-2 text-lg"
                    >
                        Crear nuevo cartel
                    </Button>
                </>
            ) : (
                <p className="text-gray-600 mt-2">
                    Inicia sesión para crear y gestionar tus carteles.
                </p>
            )}
        </div>
    );
};

export default Home;
