import { Activity } from "react";
import { Fragment, useEffect, useState } from "react";
import { Formik } from "formik";
import { Form, Button, Card, Row, Col, Spinner, Accordion } from "react-bootstrap";
import CenteredCard from "../displays/CenteredCard";
import { useNavigate, useParams } from "react-router-dom";

import InputFormik from "../forms/InputFormik";
import PasswordFormik from "../forms/PasswordFormik";
import SwitchFormik from "../forms/SwitchFormik";

import { UsuarioSchema } from "./UsuarioSchema";
import {
  obtenerUsuario,
  crearUsuario,
  editarUsuario,
} from "../../api/UsuariosAPI";

export default function UsuarioForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  const [cargando, setCargando] = useState(true);

  const [initialValues, setInitialValues] = useState({
    username: "",
    email: "",
    activo: true,

    // Datos personales
    nombres: "",
    apellidos: "",
    dni: "",
    telefono: "",
    direccion: "",
    email_contacto: "",

    // Profesional
    matricula: "",
    especialidad: "",

    // Passwords solo en creación
    password: "",
    password2: "",
  });

  const validationSchema = UsuarioSchema(isEdit);

  // 🔹 Cargar datos del usuario si es edición
  useEffect(() => {
    const cargarUsuario = async () => {
      if (!isEdit) {
        setCargando(false);
        return;
      }

      try {
        const data = await obtenerUsuario(id);

        setInitialValues({
          username: data.username,
          email: data.email,
          activo: data.activo,

          nombres: data.nombres || "",
          apellidos: data.apellidos || "",
          dni: data.dni || "",
          telefono: data.telefono || "",
          direccion: data.direccion || "",
          email_contacto: data.email_contacto || "",

          matricula: data.matricula || "",
          especialidad: data.especialidad || "",

          password: "",
          password2: "",
        });
      } catch (error) {
        console.error("Error cargando usuario", error);
      } finally {
        setCargando(false);
      }
    };

    cargarUsuario();
  }, [id, isEdit]);

  const onSubmit =
    (isEdit, id, navigate) =>
    async (values) => {
      try {
        if (isEdit) {
          await editarUsuario(id, values);
        } else {
          await crearUsuario(values);
        }

        navigate("/usuarios");
      } catch (error) {
        console.error("Error guardando usuario:", error);
      }
    };

  if (cargando)
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" />
      </div>
    );

  return (
    <Fragment>

    {initialValues.rol === "medico" && (
        <CenteredCard className="shadow-sm mt-4 border-success">
          <Card.Body className="d-flex justify-content-between align-items-center">
            <div>
              <h5 className="text-success mb-1">Turnos del día</h5>
              <div className="text-muted">Acceso rápido a tu agenda de hoy</div>
            </div>

            <Button
              variant="success"
              onClick={() => {
                const hoy = new Date().toISOString().slice(0, 10);
                navigate(`/turnos?medico_id=${id}&fecha_inicial=${hoy}`);
              }}
            >
              Ver turnos
            </Button>
          </Card.Body>
        </CenteredCard>
      )}
      <Formik
        key={id ?? "create"}
        initialValues={initialValues}
        enableReinitialize
        validationSchema={validationSchema}
        onSubmit={onSubmit(isEdit, id, navigate)}
      >
        {(formik) => (
          <CenteredCard className="shadow-sm mt-4 mb-4">
            <Card.Body>
              <h3 className="mb-4">
                {isEdit ? "Editar Usuario" : "Crear Usuario"}
              </h3>

              <Form onSubmit={formik.handleSubmit}>
                <Accordion defaultActiveKey="0">
                {/* 🟦 Datos de cuenta */}
                <Accordion.Item eventKey="0">
                <Accordion.Header>Datos de la cuenta</Accordion.Header>
                <Accordion.Body>
                  <Activity>
                    <Row>
                      <Col md={6}>
                        <InputFormik
                          name="username"
                          label="Usuario"
                          placeholder="Ingresa el nombre de usuario"
                        />
                      </Col>

                      <Col md={6}>
                        <InputFormik
                          name="email"
                          type="email"
                          label="Email de acceso"
                          placeholder="usuario@gmail.com"
                        />
                      </Col>
                    </Row>

                    <Row className="mt-3">
                      <Col md={6} className="d-flex align-items-center">
                        <SwitchFormik name="activo" label="Usuario activo" />
                      </Col>
                    </Row>

                {!isEdit && (
                  <Row className="mt-3">
                    <Col md={6}>
                      <PasswordFormik
                        name="password"
                        label="Contraseña"
                        placeholder="Contraseña"
                      />
                    </Col>

                    <Col md={6}>
                      <PasswordFormik
                        name="password2"
                        label="Repetir contraseña"
                        placeholder="Repite contraseña"
                      />
                    </Col>
                  </Row>
                )}
                  </Activity>
                </Accordion.Body>
              </Accordion.Item>

                {/* 🟦 Datos personales */}
                <Accordion.Item eventKey="1">
                  <Accordion.Header>Datos personales</Accordion.Header>
                  <Accordion.Body>
                    <Activity>

                <Row>
                  <Col md={6}>
                    <InputFormik
                      name="nombres"
                      label="Nombres"
                      placeholder="Juan Carlos"
                    />
                  </Col>
                  <Col md={6}>
                    <InputFormik
                      name="apellidos"
                      label="Apellidos"
                      placeholder="Pérez Gómez"
                    />
                  </Col>
                </Row>

                <Row className="mt-3">
                  <Col md={4}>
                    <InputFormik
                      name="dni"
                      label="DNI"
                      placeholder="12345678"
                    />
                  </Col>

                  <Col md={4}>
                    <InputFormik
                      name="telefono"
                      label="Teléfono"
                      placeholder="351555555"
                    />
                  </Col>

                  <Col md={4}>
                    <InputFormik
                      name="email_contacto"
                      label="Email de contacto"
                      placeholder="contacto@gmail.com"
                    />
                  </Col>
                </Row>

                <Row className="mt-3">
                  <Col md={12}>
                    <InputFormik
                      name="direccion"
                      label="Dirección"
                      placeholder="Calle Falsa 123"
                    />
                  </Col>
                </Row>
                </Activity>
                </Accordion.Body>
              </Accordion.Item>

                {/* 🟩 Datos profesionales (solo médicos) */}
                {formik.values.rol === "medico" && (
                  <>
                    
                    <Accordion.Item eventKey="2">
                <Accordion.Header>Datos profesionales</Accordion.Header>
                <Accordion.Body>
                  <Activity>
                    <Row>
                      <Col md={6}>
                        <InputFormik
                          name="matricula"
                          label="Matrícula"
                          placeholder="M-12345"
                        />
                      </Col>

                      <Col md={6}>
                        <InputFormik
                          name="especialidad"
                          label="Especialidad"
                          placeholder="Odontología general / Ortodoncia"
                        />
                      </Col>
                    </Row>
                     </Activity>
                    </Accordion.Body>
                  </Accordion.Item>
                  </>
                )}
                </Accordion>

                {/* Submit */}
                <div className="d-flex justify-content-end mt-4">
                  <Button type="submit" variant="primary" size="lg">
                    Guardar
                  </Button>
                </div>
              </Form>
            </Card.Body>
          </CenteredCard>
        )}
      </Formik>
    </Fragment>
  );
}
