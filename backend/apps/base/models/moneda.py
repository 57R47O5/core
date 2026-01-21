from django.db import models
from framework.models.basemodels import Constant, ConstantModel, ConstantModelManager

class MonedaManager(ConstantModelManager):
    """
    Manager de Moneda que expone las constantes del dominio
    como atributos de acceso directo.

    Cada constante representa una instancia persistida del
    modelo Moneda, identificada de forma estable por su
    `codigo` y no por su clave primaria (id).

    Este enfoque permite:
    - Evitar el uso de IDs hardcodeados en el código
    - Garantizar portabilidad entre proyectos y clientes
    - Mantener una semántica de dominio explícita
    - Reutilizar el mismo código independientemente del
      estado o del orden de carga de la base de datos

    Las constantes se definen utilizando el descriptor
    `Constant`, que resuelve y cachea la instancia
    correspondiente desde la base de datos.

    Ejemplo de uso:

        moneda = Moneda.objects.GUARANI
        simbolo = Moneda.objects.DOLAR.simbolo

    Las instancias retornadas son objetos reales del modelo
    Moneda y pueden utilizarse como cualquier otra instancia
    de Django ORM.
    """
    GUARANI = Constant("PYG")
    DOLAR = Constant("USD")
    REAL = Constant("BRL")


class Moneda(ConstantModel):
    """
    Modelo de dominio que representa una moneda del sistema.

    Moneda es un modelo de tipo constante, lo que significa
    que sus instancias principales:
    - Son identificadas por un `codigo` estable (ej: PYG, USD)
    - Existen como conceptos del dominio antes que como
      registros accidentales de base de datos
    - Son reutilizables y portables entre proyectos

    Este modelo hereda de `ConstantModel`, por lo que incluye:
    - Auditoría (created/updated, usuarios)
    - Soft delete
    - Históricos
    - Ordenamiento consistente por nombre

    El acceso a las monedas constantes debe realizarse a
    través del manager:

        Moneda.objects.GUARANI
        Moneda.objects.DOLAR

    y no mediante consultas por clave primaria.
    """
    simbolo = models.CharField(max_length=5)

    objects = MonedaManager()

    class Meta:
        db_table = "moneda"
        managed = False
