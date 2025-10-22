import FormularioCartel from "../components/Carteles/FormularioCartel";
import axiosClient from "../api/axiosClient";

const CrearCartelPage = () => {
  const crearCartel = async (data) => {
    try {
      const response = await axiosClient.post("/api/carteles/", data);
      alert("Cartel creado correctamente");
      console.log(response.data);
    } catch (error) {
      console.error("Error al crear cartel", error);
    }
  };

  return (
    <div className="container mt-4">
      <h3>Registrar nuevo cartel</h3>
      <FormularioCartel onSubmit={crearCartel} />
    </div>
  );
};

export default CrearCartelPage;
