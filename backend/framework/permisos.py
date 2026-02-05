from framework.models.basemodels import ConstantModelManager, Constant

class Perm:
    def evaluate(self, permisos: set[str]) -> bool:
        raise NotImplementedError

    def collect(self) -> set["AtomicPerm"]:
        """
        Devuelve todos los permisos atómicos involucrados
        en esta expresión.
        """
        raise NotImplementedError

    def __and__(self, other: "Perm") -> "Perm":
        return AndPerm(self, other)

    def __or__(self, other: "Perm") -> "Perm":
        return OrPerm(self, other)

class AtomicPerm(Perm):
    def __init__(self, code: str):
        self.code = code

    def P(constant: Constant) -> Perm:
        return Perm(constant.codigo)

    def evaluate(self, permisos: set[str]) -> bool:
        return self.code in permisos

    def collect(self) -> set["AtomicPerm"]:
        return {self}

    def __repr__(self):
        return f"Perm({self.code})"
    

class AndPerm(Perm):
    def __init__(self, left: Perm, right: Perm):
        self.left = left
        self.right = right

    def evaluate(self, permisos):
        return self.left.evaluate(permisos) and self.right.evaluate(permisos)

    def collect(self):
        return self.left.collect() | self.right.collect()


class OrPerm(Perm):
    def __init__(self, left: Perm, right: Perm):
        self.left = left
        self.right = right

    def evaluate(self, permisos):
        return self.left.evaluate(permisos) or self.right.evaluate(permisos)

    def collect(self):
        return self.left.collect() | self.right.collect()


def require_perm(perm: Perm):
    """
    Declara el permiso requerido para una action.
    """
    def decorator(func):
        setattr(func, "_required_perm", perm)
        return func
    return decorator



class PermisoManager(ConstantModelManager):
    """
    Manager que expone permisos como constantes del dominio.
    Cada App debe heredar de este Manager
    class PermisosBase(PermisoManager):
        BASE_PERSONA_VIEW = Constant("base.persona.view")
        BASE_PERSONA_EDIT = Constant("base.persona.edit")
        BASE_EMPRESA_VIEW = Constant("base.empresa.view")
    """
    ...

