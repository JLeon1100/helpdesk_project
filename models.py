# ==============================================================================
# MÓDULO: models.py
# Capa de Lógica de Negocio y Persistencia de Datos (POO + JSON)
# ==============================================================================

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

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

        self.ticket_id: int = ticket_id
        self.user_name: str = user_name
        self.description: str = description
        self.category: str = category
        self.priority: str = priority
        self.status: str = status

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

        self.file_path: str = file_path
        self.tickets: List[Ticket] = []
        #self.load_from_json()