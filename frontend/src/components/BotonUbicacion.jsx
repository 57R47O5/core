function UseCurrentLocation({ onChange }) {
  const handleClick = () => {
    navigator.geolocation.getCurrentPosition(pos => {
      onChange({
        lat: pos.coords.latitude,
        lon: pos.coords.longitude,
      });
    });
  };

  return (
    <Button variant="secondary" onClick={handleClick}>
      Usar mi ubicación
    </Button>
  );
}

<Button
  variant="danger"
  onClick={() => helpers.setValue(null)}
>
  Eliminar punto
</Button>