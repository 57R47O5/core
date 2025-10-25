import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const MapaUbicacion = ({ latitudInicial, longitudInicial, onUbicacionChange }) => {
    const [posicion, setPosicion] = useState([latitudInicial, longitudInicial]);

    const MarcadorSeleccion = () => {
        useMapEvents({
            click(e) {
                const { lat, lng } = e.latlng;
                setPosicion([lat, lng]);
                onUbicacionChange({lat, lng});
            },
        });

        return posicion === null ? null : (
            <Marker position={posicion}>
                <Popup>
                    Ubicación seleccionada: {posicion[0]}, {posicion[1]}
                </Popup>
            </Marker>
        );
    };

    console.log('latitudInicial: ', latitudInicial)
    console.log('longitudInicial: ', longitudInicial)
    return (
        <MapContainer center={posicion} zoom={13} style={{ height: "400px", width: "100%" }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            <MarcadorSeleccion />
        </MapContainer>
    );
};

export default MapaUbicacion;