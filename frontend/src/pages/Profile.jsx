import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import PersonaForm from "../components/personas/PersonaForm";
import { getPersona } from "../api/PersonasAPI";

const Profile = () => {
  const { user, persona } = useContext(AuthContext);
  const [datosPersona, setDatosPersona] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadPersona = async () => {
      if (!user) return;
      setLoading(true);

      let data = null;
      if (persona) {
        data = await getPersona(persona);
      }

      setDatosPersona(data);
      setLoading(false);
    };

    loadPersona();
  }, [user, persona]);

  const handleSuccess = async () => {
    if (!persona) return;
    const data = await getPersona(persona);
    setDatosPersona(data);
  };

  if (!user) return <p>Cargando usuario...</p>;
  if (loading) return <p>Cargando datos del perfil...</p>;

  // 🔹 Solo mostramos el formulario una vez que terminó la carga
  return (
    <div className="perfil-container" style={{ maxWidth: 600, margin: "0 auto" }}>
      {datosPersona !== null ? (
        // Modo visualización / edición
        <PersonaForm user={user} datosPersona={datosPersona} onSuccess={handleSuccess} />
      ) : (
        // Modo creación
        <PersonaForm user={user} datosPersona={null} onSuccess={handleSuccess} />
      )}
    </div>
  );
};

export default Profile;
