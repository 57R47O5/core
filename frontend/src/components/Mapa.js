import { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from "leaflet";

const iconoSeleccion = new L.DivIcon({
    html: "<div style='font-size:24px;'>📍</div>",
    iconSize: [24, 24],
    className: "marker-seleccion", 
});

const MapaUbicacion = ({ latitudInicial, longitudInicial, onUbicacionChange, children }) => {
    const [posicion, setPosicion] = useState([latitudInicial, longitudInicial]);

    const MarcadorSeleccion = () => {
        useMapEvents({
            click(e) {
                const { lat, lng } = e.latlng;
                setPosicion([lat, lng]);
                onUbicacionChange({ lat, lng });
            },
        });

        return (
            <Marker position={posicion} icon={iconoSeleccion}>
                <Popup>
                    Ubicación seleccionada: {posicion[0]}, {posicion[1]}
                </Popup>
            </Marker>
        );
    };

    return (
        <MapContainer center={posicion} zoom={13} style={{ height: "400px", width: "100%" }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            <MarcadorSeleccion />
            {children}
        </MapContainer>
    );
};

export default MapaUbicacion;
