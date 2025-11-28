import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import {MapaNuevoCartel} from "./MapaCarteles";
import SelectFormik from "../forms/SelectFormik";

const schema = Yup.object().shape({
  tipo_cartel: Yup.string().required("El tipo de cartel es obligatorio"),
  precio: Yup.number().nullable(),
  ancho_metros: Yup.number().required("Campo obligatorio"),
  alto_metros: Yup.number().required("Campo obligatorio"),
});

const FormularioCartel = ({ onSubmit }) => {
  return (
    <Formik
      initialValues={{
        tipo_cartel: "",
        precio: "",
        ancho_metros: "",
        alto_metros: "",
        latitud: "",
        longitud: "",
      }}
      validationSchema={schema}
      onSubmit={(values) => onSubmit(values)}
    >
      {({ setFieldValue }) => (
        <Form>
          <div className="mb-3">
            <label>Tipo de Cartel</label>
            <SelectFormik 
            name='tipo_cartel'
            endpoint='tipo-carteles'
            />
          </div>

          <div className="row">
            <div className="col">
              <label>Ancho (m)</label>
              <Field name="ancho_metros" type="number" className="form-control" />
            </div>
            <div className="col">
              <label>Alto (m)</label>
              <Field name="alto_metros" type="number" className="form-control" />
            </div>
          </div>

          <div className="mb-3">
            <label>Precio (opcional)</label>
            <Field name="precio" type="number" className="form-control" />
          </div>

          <div className="mb-3">
            <label>Ubicación</label>
            <MapaNuevoCartel
              onUbicacionSeleccionada={(latlng) => {
                setFieldValue("latitud", latlng.lat);
                setFieldValue("longitud", latlng.lng);
              }}
            />
            <div className="text-muted">
              Lat: <Field name="latitud" disabled /> — Lng: <Field name="longitud" disabled />
            </div>
          </div>

          <button type="submit" className="btn btn-primary mt-3">
            Guardar Cartel
          </button>
        </Form>
      )}
    </Formik>
  );
};

export default FormularioCartel;
