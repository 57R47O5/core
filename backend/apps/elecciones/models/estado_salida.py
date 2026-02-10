from framework.models.basemodels import Constant, ConstantModel, ConstantModelManager

class EstadoSalidaManager(ConstantModelManager):
    PLANIFICADA=Constant("Planificada")
    EN_CURSO=Constant("En Curso")
    FINALIZADA=Constant("Finalizada")
    CANCELADA=Constant("Cancelada")

class EstadoSalida(ConstantModel):
    """
    Estado operativo de una salida
    """
    objects = EstadoSalidaManager()

    class Meta:
        db_table = "estado_salida"
        managed = False
