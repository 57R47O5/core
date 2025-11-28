import { useEffect, useState } from "react";
import { Formik } from "formik";
import { Form, Button, Row, Col, Card } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";

import InputFormik from "../forms/InputFormik";
import PasswordFormik from "../forms/PasswordFormik";
import SwitchFormik from "../forms/SwitchFormik";
import SelectFormik from "../forms/SelectFormik";

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

  const [initialValues, setInitialValues] = useState({
    username: "",
    email: "",
    rol: "",
    password: "",
    password2: "",
    activo: true,
  });

  const validationSchema = UsuarioSchema(isEdit);

  // 🔹 Cargar datos si es edición
  useEffect(() => {
    const cargarUsuario = async () => {
      if (isEdit) {
        const data = await obtenerUsuario(id);
        setInitialValues({
          username: data.username,
          email: data.email,
          rol: data.rol,
          password: "",
          password2: "",
          activo: data.activo,
        });
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

  return (
    <Formik
      key={id ?? "create"}
      initialValues={initialValues}
      enableReinitialize
      validationSchema={validationSchema}
      onSubmit={onSubmit(isEdit, id, navigate)}
    >
      {(formik) => (
        <Card className="shadow-sm mt-4">
          <Card.Body>
            <h3 className="mb-4">
              {isEdit ? "Editar usuario" : "Crear usuario"}
            </h3>

            <Form onSubmit={formik.handleSubmit}>
              <Row>
                <Col md={6}>
                  <InputFormik
                    name="username"
                    label="Usuario"
                    placeholder="Usuario"
                  />
                </Col>

                <Col md={6}>
                  <InputFormik
                    name="email"
                    type="email"
                    label="Email"
                    placeholder="Email"
                  />
                </Col>
              </Row>

              <Row>
                <Col md={6}>
                  <SelectFormik
                    name="rol"
                    label="Rol"
                    endpoint="usuarios/roles"
                  />
                </Col>

                <Col md={6} className="d-flex align-items-center">
                  <SwitchFormik
                    name="activo"
                    label="Activo"
                  />
                </Col>
              </Row>

              {!isEdit && (
                <Row>
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
                      placeholder="Repetir contraseña"
                    />
                  </Col>
                </Row>
              )}

              <div className="d-flex justify-content-end mt-4">
                <Button type="submit" variant="primary">
                  Guardar
                </Button>
              </div>
            </Form>
          </Card.Body>
        </Card>
      )}
    </Formik>
  );
}
