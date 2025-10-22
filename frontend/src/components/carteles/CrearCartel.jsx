import React, { useState } from "react";
import axiosClient from "../../api/axiosClient";
import MapaUbicacion from "../../components/MapaUbicacion";

const CrearCartel = () => {
  const [formData, setFormData] = useState({
    nombre: "",
    tipo_cartel: "",
    ancho: "",
    alto: "",
    latitud: null,
    longitud: null,
    precio_exhibicion: "",
  });

  const [imagenes, setImagenes] = useState([]);
  const [mensaje, setMensaje] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleUbicacionChange = (lat, lng) => {
    setFormData({
      ...formData,
      latitud: lat,
      longitud: lng,
    });
  };

  const handleFileChange = (e) => {
    setImagenes(e.target.files);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const data = new FormData();
      Object.entries(formData).forEach(([key, value]) => {
        data.append(key, value);
      });

      for (let i = 0; i < imagenes.length; i++) {
        data.append("imagenes", imagenes[i]);
      }

      const response = await axiosClient.post("/api/carteles/", data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setMensaje("✅ Cartel creado correctamente");
      console.log("Respuesta del servidor:", response.data);
    } catch (error) {
      console.error("Error al crear cartel:", error);
      setMensaje("❌ Error al crear el cartel");
    }
  };

  return (
    <div className="container mt-4">
      <h2>Registrar nuevo cartel</h2>

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label>Nombre del cartel</label>
          <input
            type="text"
            name="nombre"
            className="form-control"
            value={formData.nombre}
            onChange={handleChange}
          />
        </div>

        <div className="mb-3">
          <label>Tipo de cartel</label>
          <input
            type="text"
            name="tipo_cartel"
            className="form-control"
            value={formData.tipo_cartel}
            onChange={handleChange}
          />
        </div>

        <div className="row">
          <div className="col">
            <label>Ancho (m)</label>
            <input
              type="number"
              name="ancho"
              className="form-control"
              value={formData.ancho}
              onChange={handleChange}
            />
          </div>
          <div className="col">
            <label>Alto (m)</label>
            <input
              type="number"
              name="alto"
              className="form-control"
              value={formData.alto}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="mt-4">
          <h5>Seleccionar ubicación en el mapa</h5>
          <MapaUbicacion
            latitudInicial={-25.2964}
            longitudInicial={-57.647}
            onUbicacionChange={handleUbicacionChange}
          />
          {formData.latitud && (
            <p className="mt-2">
              📍 Coordenadas seleccionadas: {formData.latitud}, {formData.longitud}
            </p>
          )}
        </div>

        <div className="mt-3">
          <label>Precio de exhibición (opcional)</label>
          <input
            type="number"
            name="precio_exhibicion"
            className="form-control"
            value={formData.precio_exhibicion}
            onChange={handleChange}
          />
        </div>

        <div className="mt-3">
          <label>Imágenes del cartel</label>
          <input
            type="file"
            multiple
            className="form-control"
            onChange={handleFileChange}
          />
        </div>

        <button type="submit" className="btn btn-primary mt-4">
          Guardar Cartel
        </button>
      </form>

      {mensaje && <p className="mt-3">{mensaje}</p>}
    </div>
  );
};

export default CrearCartel;
