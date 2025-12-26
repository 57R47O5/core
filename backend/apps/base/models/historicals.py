import warnings

from django.db.models import signals
from simple_history.models import HistoricalRecords


class NewHistoricalRecords(HistoricalRecords):
    """
    Sobreescribe HistoricalRecords para los siguientes features adicionales:
        - Permite la herencia de HistoricalRecords sobreescribible entre los modelos.
        - Permite compartir HistoricalRecords en los modelos Proxy.
        - Define el "hist_" como sufijo por defecto a las tablas de todos los modelos históricos.
    """

    signal_registered = False

    def __init__(self, *args, disabled=False, **kwargs,):
        super().__init__(*args, **kwargs)
        self.disabled = disabled

    def contribute_to_class(self, cls, name):
        """
        Este código es detectado e invocado automáticamente por django cuando
        un modelo posee un atributo con una instancia de CBAHistoricalRecords.
        """

        # Asignación de atributos requeridos por HistoricalRecords
        self.manager_name = name        # pylint: disable=attribute-defined-outside-init
        self.module = cls.__module__    # pylint: disable=attribute-defined-outside-init
        self.cls = cls                  # pylint: disable=attribute-defined-outside-init
        self.add_extra_methods(cls)

        # Códigos sobreescritos del CBAHistoricalRecords

        # Si la función 'invoke_finalize' no fué registrada
        # en signals.class_prepared
        is_registered = False
        for _, receiver in signals.class_prepared.receivers:
            if receiver is self.invoke_finalize:
                is_registered = True
        if not is_registered:
            # Registrar la función 'invoke_finalize' en la signals.class_prepared
            signals.class_prepared.connect(
                self.invoke_finalize, weak=False)

        # Asignar/reasignar la instancia CBAHistoricalRecords actual
        # al modelo 'cls'.
        setattr(cls, '_cba_historical_records', self)

        # Warning del HistoricalRecords
        if cls._meta.abstract and not self.inherit:
            msg = (
                "HistoricalRecords added to abstract model ({}) without "
                "inherit=True".format(self.cls.__name__)
            )
            warnings.warn(msg, UserWarning)

    @staticmethod
    def invoke_finalize(sender, **kwargs):
        # En esta función se decide si el modelo tendrá un modelo histórico

        conditions_are_met = (
            # el modelo tiene un CBAHistoricalRecords
            hasattr(sender, '_cba_historical_records')
            # el modelo no tiene el history desactivado
            and (not getattr(sender, '_cba_historical_records').disabled))

        if conditions_are_met:
            # invoca el 'finalize' del correspondiente modelo 'sender' para
            # registrar dinámicamente el correspondiente modelo histórico.

            # pylint: disable=protected-access
            sender._cba_historical_records.finalize(sender, **kwargs)

    def get_meta_options(self, model):
        """
        Returna los meta atributos adicionales del modelo.
        """

        meta_fields = super().get_meta_options(model)

        # Si no está definido un nombre para la tabla,
        if self.table_name is None:
            original_table_name = str(model._meta.db_table).lower()
            if original_table_name.startswith('rrhh_'):
                # Reemplaza el prefijo 'rrhh_' por 'hist_'
                meta_fields['db_table'] = 'hist_' + original_table_name[5:]
            else:
                # Agrega el prefijo 'hist_'
                meta_fields['db_table'] = 'hist_' + original_table_name

        if model._meta.proxy:
            meta_fields['proxy'] = True

        return meta_fields

    def create_history_model(self, model, inherited):
        """
        Crea un modelo histórico dinámicamente a partir de un modelo
        """
        # Si el modelo es de tipo proxy
        if model._meta.proxy:
            # Obtiene el modelo ancestro más cercano que no es un proxy
            non_proxy_ancestor = None
            for ancestor_model in model.mro():
                if not ancestor_model._meta.proxy:
                    non_proxy_ancestor = ancestor_model
                    break

            name = self.get_history_model_name(model)

            # Crea un modelo histórico proxy a partir del modelo histórico de model
            parent_history_model = getattr(
                non_proxy_ancestor, self.manager_name).model
            history_model = type(str(name), (parent_history_model,), {
                "__module__": model.__module__,
                "Meta": type(str("Meta"), (), {
                    "proxy": "True"
                })
            })

            return history_model
        else:
            return super().create_history_model(model, inherited)

    def post_delete(self, instance, using=None, **kwargs):
        if self.cascade_delete_history:
            manager = getattr(instance, self.manager_name)
            manager.using(using).all().delete()
        else:
            # TODO Tadashi: Parche para fast-delete
            if hasattr(instance, 'history_bulk_delete'):
                return
            self.create_historical_record(instance, "-", using=using)
