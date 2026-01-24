from framework.models.basemodels import BaseModel

class Persona(BaseModel):
    
    class Meta:
        db_table = "persona"
        managed = False

    @property
    def fisica(self):
        return getattr(self, "personafisica", None)

    @property
    def juridica(self):
        return getattr(self, "personajuridica", None)

    @property
    def tipo(self):
        if self.fisica:
            return "FISICA"
        if self.juridica:
            return "JURIDICA"
        return None
