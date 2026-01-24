from framework.models.basemodels import (
    Constant, 
    ConstantModel, 
    ConstantModelManager)

class Manager(ConstantModelManager):
    CEDULA = Constant("CI")
    RUC = Constant("RUC")
    PASAPORTE = Constant("Pasaporte")

class TipoDocumentoIdentidad(ConstantModel):
    objects = Manager()

    class Meta:
        db_table = "tipo_documento_identidad"
        managed = False