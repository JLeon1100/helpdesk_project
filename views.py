# ==============================================================================
# MÓDULO: views.py
# Capa de Interfaz Gráfica de Usuario (Tkinter y TTK)
# ==============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from models import TicketManager

# **************************************************
# CLASE PRINCIPAL DE LA INTERFAZ (HELPDESK APP VIEW)
# **************************************************

#Construye y gestiona los componentes de la interfaz de usuario
class HelpdeskView(ttk.Frame):
    """
    Clase que representa y gestiona la interfaz gráfica principal de la aplicación DataDesk.

    Attributes:
        master (tk.Tk): Ventana principal o contenedor raíz de Tkinter.
        manager (TicketManager): Instancia del gestor de datos para operar el CRUD.
    """

    def __init__(self, master: tk.Tk, manager) -> None:
        """
        Inicializa la vista de la aplicación y sus componentes gráficos.
        """

        super().__init__(master)
        self.master: tk.Tk = master
        self.manager = manager

        # Configuración de la ventana principal
        self.master.title("DataDesk - Sistema de Gestión de Tickets Helpdesk")
        self.master.geometry("1000x650")
        self.master.minsize(850, 550)

        self.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Inicialización de componentes visuales
        #self._create_widgets()
        #self.refresh_table()
        #self.update_metrics()