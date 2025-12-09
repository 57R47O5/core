import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Form as RBForm, Button, Row, Col } from "react-bootstrap";
import CenteredCard from "../displays/CenteredCard";
import SelectFormik from "../forms/SelectFormik";
import DatePickerFormik from "../forms/DatePickerFomik";
import FormikAutocompleteRemote from "../forms/FormikAutocompleteRemote";
import {crear} from "./TurnoAPI"

const TurnoSchema = Yup.object().shape({
  fecha_inicio: Yup.string().required("Ingrese una fecha"),
  odontologo: Yup.string().required("Seleccione un médico"),
  paciente: Yup.string().required("Ingrese el nombre del paciente"),
});

const TurnoCrear = () => {

  return (
    <CenteredCard className="p-4 mt-4">
      <h3 className="mb-4 text-center">Crear turno</h3>

      <Formik
        initialValues={{
          fecha_inicio: "",
          odontologo: "",
          paciente: "",
        }}
        validationSchema={TurnoSchema}
        onSubmit={async (values, { setSubmitting, resetForm }) => {
          try {
              console.log("Enviando turno...", values);

              const respuesta = await crear(values);

              console.log("Respuesta del backend:", respuesta);

              alert("Turno creado correctamente.");

              resetForm();
          } catch (error) {
              console.error("Error creando el turno", error);
              alert("Hubo un error al crear el turno.");
          } finally {
              setSubmitting(false);
          }
      }}
      >
        {() => (
          <Form>
            <Row className="mb-3">
              <Col md={6}>
                <RBForm.Label>Fecha Inicio</RBForm.Label>
                <DatePickerFormik name="fecha_inicio" mode="datetime" />
              </Col>
            </Row>

            <RBForm.Label>Médico</RBForm.Label>
            <SelectFormik
              name="odontologo"
              endpoint='usuarios/medicos'
              placeholder="Seleccione un médico"
            />

            <hr />

            <h5>Datos del paciente</h5>

            <RBForm.Label>Nombre completo</RBForm.Label>
            <FormikAutocompleteRemote
              name="paciente"
              endpoint="pacientes"
              placeholder="Nombre del paciente"
            />

            <div className="text-center mt-3">
              <Button type="submit" variant="primary">
                Crear turno
              </Button>
            </div>
          </Form>
        )}
      </Formik>
    </CenteredCard>
  );
};

export default TurnoCrear;
