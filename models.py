# ==============================================================================
# MÓDULO: models.py
# Capa de Lógica de Negocio y Persistencia de Datos (POO + JSON)
# ==============================================================================

import json # Permite trabajar con archivos JSON
import os # Permite validar si existen archivos
from pathlib import Path # Manejo de rutas de archivos
from typing import List, Dict, Any, Optional # Tipado para mejorar la legibilidad del código

# **************************************************
# CLASE TICKET (ENTIDAD PRINCIPAL)
# **************************************************

class Ticket:
    """
    Representa la entidad individual de una incidencia dentro del sistema DataDesk.
    Attributes:
        ticket_id (int): Identificador único del ticket.
        user_name (str): Nombre del usuario o empleado que reporta la incidencia.
        description (str): Detalle técnico o explicación del problema.
        category (str): Categoría de la incidencia (ej: Hardware, Software, Redes).
        priority (str): Nivel de urgencia (Baja, Media, Alta, Crítica).
        status (str): Estado actual del ticket (Pendiente o Resuelto).
    """

    # __init__ metodo constructor, se ejecuta al crear un objeto de una clase para inicializar sus atributos
    def __init__(
        self,
        ticket_id: int,
        user_name: str,
        description: str,
        category: str,
        priority: str,
        status: str = "Pendiente"
    ) -> None:
        """
        Inicializa una nueva instancia de la clase Ticket.

        Args:
            ticket_id (int): Identificador único numérico.
            user_name (str): Nombre del usuario.
            description (str): Descripción de la falla o solicitud.
            category (str): Categoría del ticket.
            priority (str): Prioridad asignada.
            status (str, optional): Estado inicial. Por defecto es 'Pendiente'.
        """

        # Guarda la información del ticket
        self.ticket_id: int = ticket_id
        self.user_name: str = user_name
        self.description: str = description
        self.category: str = category
        self.priority: str = priority
        self.status: str = status

    # to_dict convierte un objeto o estructura de datos en un diccionario estándar
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto Ticket a un diccionario para almacenamiento JSON.

        Returns:
            Dict[str, Any]: Diccionario con las propiedades del ticket.
        """
        return {
            "ticket_id": self.ticket_id,
            "user_name": self.user_name,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Ticket":
        """
        Crea una instancia de Ticket a partir de un diccionario.
        Args:
            data (Dict[str, Any]): Diccionario con la información del ticket.

        Returns:
            Ticket: Nueva instancia reconstruida del objeto Ticket.
        """

        # Reconstruye un objeto Ticket desde un diccionario
        return cls(
            ticket_id=data["ticket_id"],
            user_name=data["user_name"],
            description=data["description"],
            category=data["category"],
            priority=data["priority"],
            status=data.get("status", "Pendiente")
        )

# **************************************************
# CLASE TICKETMANAGER (GESTOR DE DATOS Y CRUD)
# **************************************************

class TicketManager:
    """
    Esqueleto del gestor de datos para permitir la importación en main.py.
    Clase responsable de administrar la lista general de tickets, realizar operaciones
    CRUD y gestionar la persistencia en el archivo local 'tickets.json'.

    Attributes:
        file_path (str): Ruta del archivo JSON de almacenamiento.
        tickets (List[Ticket]): Lista en memoria de todos los objetos Ticket.
    """

    def __init__(self, file_path: str = "tickets.json") -> None:
        """
        Inicializa el gestor de tickets y carga los datos existentes.

         Args:
              file_path (str, optional): Nombre o ruta del archivo de persistencia.
         """

        self.file_path: str = file_path # Guarda la ubicación del archivo
        self.tickets: List[Ticket] = [] # Inicializa la lista de tickets
        self.load_from_json() # Carga los datos existentes

    # ==================================================
    # MÉTODOS DE PERSISTENCIA (LECTURA Y ESCRITURA JSON)
    # ==================================================

    # json.load() Leer y transformar datos de texto JSON en objetos legibles de Python
    def load_from_json(self) -> None:
        """
        Carga el archivo JSON local y reconstruye los objetos en memoria.
        Si el archivo no existe, inicializa una lista vacía de forma segura.
        """
        # Si el archivo no existe, inicia vacío
        if not os.path.exists(self.file_path):
            self.tickets = []
            return

        try:
            # Abre el archivo para leer los datos
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                # Convierte cada registro en un objeto Ticket
                self.tickets = [Ticket.from_dict(item) for item in data]
        # Si ocurre un error, limpia la lista
        except (json.JSONDecodeError, KeyError, Exception) as error:
            print(f"Error al intentar cargar el archivo de datos: {error}")
            self.tickets = []

    def save_to_json(self) -> bool:
        """
        Guarda el estado actual de la lista de tickets en el archivo JSON.

        Returns:
            bool: True si la operación fue exitosa, False en caso de error.
        """
        try:
            # Convierte todos los tickets a diccionarios
            dict_data = [ticket.to_dict() for ticket in self.tickets]
            # Guarda la información en el archivo / UTF-8 codificación de caracteres
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(dict_data, file, indent=4, ensure_ascii=False)
            return True
        # Informa si hubo un problema al guardar
        except Exception as error:
            print(f"Error al intentar guardar los datos en el archivo: {error}")
            return False

    # ==================================================
    # OPERACIONES CRUD Y BÚSQUEDA DE REGISTROS
    # ==================================================

    def _generate_new_id(self) -> int:
        """
        Genera un identificador único correlativo para cada nuevo ticket registrado.

        Returns:
            int: Nuevo código ID disponible (empezando desde 101).
        """
        # Si no hay tickets, comienza desde el 101
        if not self.tickets:
            return 101
        # Genera el siguiente ID disponible
        return max(ticket.ticket_id for ticket in self.tickets) + 1

    def create_ticket(
        self,
        user_name: str,
        description: str,
        category: str,
        priority: str
    ) -> Ticket:
        """
        Crea un nuevo ticket, lo añade a la memoria y guarda en el archivo JSON.

        Args:
            user_name (str): Nombre del usuario.
            description (str): Descripción detallada del incidente.
            category (str): Categoría seleccionada.
            priority (str): Nivel de prioridad asignado.

        Returns:
            Ticket: Objeto Ticket recién creado.
        """
        # Obtiene un nuevo identificador
        new_id = self._generate_new_id()
        # Crea el nuevo ticket
        new_ticket = Ticket(
            ticket_id=new_id,
            user_name=user_name,
            description=description,
            category=category,
            priority=priority,
            status="Pendiente"
        )
        # Lo agrega a la lista
        self.tickets.append(new_ticket)
        # Guarda los cambios
        self.save_to_json()
        return new_ticket

    def get_all_tickets(self) -> List[Ticket]:
        """
        Obtiene la lista completa de tickets almacenados.

        Returns:
            List[Ticket]: Lista de todos los objetos Ticket.
        """
        return self.tickets

    def get_ticket_by_id(self, ticket_id: int) -> Optional[Ticket]:
        """
        Busca un ticket específico mediante su número identificador ID.

        Args:
            ticket_id (int): Identificador a buscar.

        Returns:
            Optional[Ticket]: Objeto Ticket si existe, o None si no se encuentra.
        """
        # Recorre todos los tickets
        for ticket in self.tickets:
            # Devuelve el ticket si encuentra el ID
            if ticket.ticket_id == ticket_id:
                return ticket
        return None

    def update_status(self, ticket_id: int, new_status: str) -> bool:
        """
        Actualiza el estado de un ticket (ejemplo: cambiar a 'Resuelto').

        Args:
            ticket_id (int): Identificador del ticket a modificar.
            new_status (str): Nuevo estado asignado.

        Returns:
            bool: True si se actualizó correctamente, False si no se encontró.
        """
        # Busca el ticket solicitado
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket:
            # Actualiza el estado si existe
            ticket.status = new_status
            # Guarda la modificación
            self.save_to_json()
            return True
        return False

    def delete_ticket(self, ticket_id: int) -> bool:
        """
        Elimina un ticket del sistema y actualiza el archivo JSON.

        Args:
            ticket_id (int): Identificador del ticket a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa, False si no existía.
        """
        # Busca el ticket
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket:
            # Lo elimina de la lista
            self.tickets.remove(ticket)
            # Actualiza el archivo
            self.save_to_json()
            return True
        return False

    def get_metrics(self) -> Dict[str, int]:
        """
        Calcula el resumen de métricas actuales del sistema.

        Returns:
            Dict[str, int]: Cantidad total, pendientes y resueltos.
        """
        total = len(self.tickets) # Cuenta el total de tickets
        pending = sum(1 for t in self.tickets if t.status == "Pendiente") # Cuenta los pendientes
        resolved = sum(1 for t in self.tickets if t.status == "Resuelto") # Cuenta los resueltos
        # Devuelve el resumen de tickets
        return {
            "total": total,
            "pending": pending,
            "resolved": resolved
        }

    def search_tickets(self, search_text: str) -> List[Ticket]:
        """
        Filtra tickets cuyo texto coincida con el nombre, categoría, prioridad,
        descripción o número de ID.

        Args:
            search_text (str): Cadena de texto a buscar.

        Returns:
            List[Ticket]: Lista de tickets que cumplen con el criterio de búsqueda.
        """
        # Elimina espacios y convierte a minúsculas
        query = search_text.strip().lower()
        # Si no hay búsqueda, devuelve todos
        if not query:
            return self.tickets

        # Busca tickets que coincidan con el texto de búsqueda
        matched_tickets = []
        # Recorre todos los tickets
        for ticket in self.tickets:
            # Comprueba coincidencias en cada campo
            match_user = query in ticket.user_name.lower()
            match_category = query in ticket.category.lower()
            match_priority = query in ticket.priority.lower()
            match_description = query in ticket.description.lower()
            match_id = query in str(ticket.ticket_id)

            if match_user or match_category or match_priority or match_description or match_id:
                # Agrega el ticket si coincide en algún campo
                matched_tickets.append(ticket)

        # Devuelve la lista filtrada
        return matched_tickets