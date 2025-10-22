// src/components/Carteles/PopupCartel.jsx
const PopupCartel = ({ cartel }) => {
  return (
    <div style={{ minWidth: "180px" }}>
      <strong>{cartel.tipo_cartel}</strong>
      <br />
      {cartel.precio && <span>💲 {cartel.precio.toLocaleString()}</span>}
      <br />
      {cartel.direccion && <span>📍 {cartel.direccion}</span>}
      <br />
      <small>Dimensiones: {cartel.ancho}×{cartel.alto} m</small>
      <br />
      {cartel.contacto && <small>📞 {cartel.contacto}</small>}
    </div>
  );
};

export default PopupCartel;
