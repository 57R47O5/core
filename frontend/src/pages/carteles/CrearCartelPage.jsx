import FormularioCartel from "../../components/carteles/FormularioCartel";
import request from "../../api/requests"

const CrearCartelPage = () => {
  const crearCartel = async (data) => {
    try {
      const response = await request.post("carteles/crear/", data);
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
