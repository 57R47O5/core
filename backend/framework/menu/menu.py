import unicodedata
from typing  import Optional, List, Dict, Any

class P:
    """
    Recibe uno o varios permisos y verifica que se encuentren en roles
    """
    def __init__(self, perm=None) -> None:
        self.perm = perm

    def evaluate(self, permisos):
        return self.perm in permisos

    def __and__(self, permiso2):
        permiso1 = self
        class PAnd(P):
            def evaluate(self, permisos):
                return permiso1.evaluate(permisos) and permiso2.evaluate(permisos)
        return PAnd()

    def __or__(self, permiso2):
        permiso1 = self
        class POr(P):
            def evaluate(self, permisos):
                return permiso1.evaluate(permisos) or permiso2.evaluate(permisos)
        return POr()


class Node():
    def __init__(self, label=None, permiso=None, icon=None, key=None, content=None, to=None) -> None:
        self.label: Optional[str] = label
        self.content: List[Node] = content or []
        self.to: Optional[str] = to
        self.permiso: Optional[str] = permiso
        self.icon: Optional[str] = icon
        self.key: Optional[int] = key


    def to_dict(self) -> dict:
        """
        Transforma el nodo a un diccionario recursivamente.
        """
        node_dict: Dict[str, Any] = {'label': self.label}
        if self.content:
            node_dict['content'] = [
                node.to_dict()
                for node in self.content]
        if self.to:
            node_dict['to'] = self.to
        if self.icon:
            node_dict['icon'] = self.icon
        if self.key:
            node_dict['key'] = self.key
        return node_dict

    def filter(self, condition_func) -> None:
        """
        Elimina recursivamente todos los hijos que no cumplan
        cierta condición.
        """
        filtered_content = []

        for child_node in self.content:
            if condition_func(child_node):
                filtered_content.append(child_node)
                child_node.filter(condition_func)

        self.content = filtered_content

    def sort_children(
        self, recursive: bool = True, exclude_labels: list = None
    ) -> None:
        """
        Ordena los nodos hijos alfabéticamente por su label.

        :param recursive: Si es True, ordena recursivamente todos los subniveles
        :param exclude_labels: Lista de labels que deben mantenerse en su posición
        original
        """
        def normalize_for_sorting(text):
            if not text:
                return ""
            # Normaliza el texto a NFD (descompone caracteres acentuados)
            normalized = unicodedata.normalize("NFD", text.lower())
            # Filtra solo caracteres ASCII (sin acentos)
            return "".join(
                char for char in normalized if unicodedata.category(char) != "Mn"
            )

        if not self.content:
            return

        exclude_labels = exclude_labels or []

        # separamos nodos excluidos y ordenables
        excluded_nodes = []
        sortable_nodes = []

        for node in self.content:
            if node.label in exclude_labels:
                excluded_nodes.append((self.content.index(node), node))
            else:
                sortable_nodes.append(node)

        # Ordenamos los nodos que se pueden ordenar alfabéticamente (case insensitive)
        sortable_nodes.sort(key=lambda n: normalize_for_sorting(n.label))

        # Reconstruimos la lista de nodos, preservando la posición de los excluidos
        if excluded_nodes:
            new_content = sortable_nodes.copy()

            for original_index, node in sorted(excluded_nodes, key=lambda x: x[0]):
                # ajustamos el indice en caso de que sea mayor al largo actual
                insert_index = min(original_index, len(new_content))
                new_content.insert(insert_index, node)

            self.content = new_content
        else:
            self.content = sortable_nodes

        # ordenamos recursivamente
        if recursive:
            for child_node in self.content:
                child_node.sort_children(recursive=True, exclude_labels=[])

    def clone(self) -> 'Node':
        """
        Hace un deep clone de los nodos y retorna la nueva instancia.
        """
        return Node(self.label,
                        content=[
                            node.clone()
                            for node in self.content],
                        to=self.to,
                        permiso=self.permiso,
                        icon=self.icon,
                        key=self.key)


def generar_menu(permisos: List[str]) -> dict:
    """
    Genera el menú según los permisos de un usuario.
    """
    # Crea una nueva instancia de menú para el usuario
    root_node = ROOT_MENU_NODE.clone()

    # Filtra los menús a mostrar según los permisos del usuario
    def mostrar_nodo(node: Node):
        if node.permiso is None:
            return True

        if isinstance(node.permiso, str):
            if node.permiso in permisos:
                return True
        elif isinstance(node.permiso, P):
            return node.permiso.evaluate(permisos)
        return False   

            
    def mostrar_nodo_valido(node: Node):
        if node.permiso is not None and not mostrar_nodo(node):
            return False

        return bool(node.to or node.content)


    root_node.filter(mostrar_nodo_valido)

    # ordenamos los nodes del menu alfabéticamente, excluyendo 'Inicio'
    root_node.sort_children(recursive=True, exclude_labels=['Inicio'])

    def agregar_key(node: Node):
        node.key = f"{node.label}:{node.to or ''}"
        for child_node in node.content:
            agregar_key(child_node)
    agregar_key(root_node)

    def nodo_visible(nodo):
        return nodo.get("label") == "Inicio" or "content" in nodo or "to" in nodo

    return [
        nodo for nodo in root_node.to_dict()["content"]
        if nodo_visible(nodo)
    ]

    
ROOT_MENU_NODE = Node("root", content=[
    Node("Inicio", icon="FaHome", to="/"),
    Node("Base", icon="FaBed", content=[
        Node("Persona", to="/persona-fisica"),
        Node("Empresa", to="/persona-juridica"),
    ]),
])