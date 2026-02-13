from typing import Optional
from framework.models.basemodels import Constant
from framework.exceptions import ExcepcionPermisos

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
    
    def _get_required_perm(self) -> Optional[Perm]:
        if isinstance(self.action, str) and hasattr(self, self.action):
            view = getattr(self, self.action)
            return getattr(view, "_required_perm", None)
        return None

class AtomicPerm(Perm):
    def __init__(self, code: str):
        self.code = code

    def evaluate(self, permisos: set[Constant]) -> bool:
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

def P(constant: Constant) -> Perm:
    '''
    Obtiene un perm a partir de una constante
    '''
    return AtomicPerm(constant.codigo)

def require_perm(attr_name: str):
    """
    Declara el atributo del controller que define el permiso requerido.
    """
    def decorator(func):
        setattr(func, "_required_perm", attr_name)
        return func
    return decorator

def check_permissions(self, request):
    perm = self._get_required_perm()
    if perm and not perm.evaluate(request.permisos):
        raise ExcepcionPermisos()
    
class PermisoGroup:
    '''
    Clase utilizada para agrupar permisos
    '''
    @classmethod
    def constants(cls) -> dict[str, Constant]:
        return {
            name: value
            for name, value in vars(cls).items()
            if isinstance(value, Constant)
        }

    @classmethod
    def all(cls):
        permisos = []

        # 1. permisos propios
        permisos.extend(
            value for value in vars(cls).values()
            if isinstance(value, Constant)
        )

        # 2. permisos de grupos
        for group in getattr(cls, "grupos", []):
            permisos.extend(group.all())

        return permisos
    
    @classmethod
    def _get_groups(cls):
        return getattr(cls, "grupos", [])
    
    @classmethod
    def to_perm(cls) -> Perm:
        """
        Crea un objeto Perm agrupando los permisos
        de la clase con OR lógico.
        """
        perms = [P(const) for const in cls.constants().values()]
        
        if not perms:
            raise ValueError(f"{cls.__name__} no define permisos.")

        expr = perms[0]
        for perm in perms[1:]:
            expr = expr | perm

        return expr