from framework.models.basemodels import Constant, ConstantModel, ConstantModelManager

class TipoContactoManager(ConstantModelManager):
    CORREO_ELECTRONICO = Constant("CORREO_ELECTRONICO")
    TELEFONO = Constant("TELEFONO")
    DIRECCION = Constant("DIRECCION")

class TipoContacto(ConstantModel):
    objects = TipoContactoManager()

    class Meta:
        managed = False
        db_table = "tipo_contacto"
        verbose_name = "Tipo de Contacto"
        verbose_name_plural = "Tipos de Contacto"