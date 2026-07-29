# ==============================================================================
# MÓDULO: views.py
# Capa de Interfaz Gráfica de Usuario (Tkinter y TTK)
# ==============================================================================

import tkinter as tk # Librerías para crear la interfaz
from tkinter import ttk, messagebox # Componentes adicionales de Tkinter
from typing import Optional # Tipado opcional
from models import TicketManager, Ticket # Importa el modelo de datos

# **************************************************
# CLASE PRINCIPAL DE LA INTERFAZ (HELPDESK APP VIEW)
# **************************************************

# Construye y gestiona los componentes de la interfaz de usuario
class HelpdeskView(ttk.Frame):
    """
    Clase que representa y gestiona la interfaz gráfica principal de la aplicación DataDesk.

    Attributes:
        master (tk.Tk): Ventana principal o contenedor raíz de Tkinter.
        manager (TicketManager): Instancia del gestor de datos para operar el CRUD
        (Create, Read, Update, Delete).
    """

    # __init__ metodo constructor, se ejecuta al crear un objeto de una clase para inicializar sus atributos
    def __init__(self, master: tk.Tk, manager: TicketManager) -> None:
        """
        Inicializa la vista de la aplicación y sus componentes gráficos.
        Args:
            master (tk.Tk): Ventana raíz de la aplicación.
            manager (TicketManager): Gestor de datos y lógica de negocio.
        """
        # super().__init__ llama metodo constructor __init__ de superclase desde una subclase,
        # permite reutilizar código y atributos heredados se inicialicen de forma correcta

        # Inicializa el Frame principal
        super().__init__(master)
        # Guarda referencias principales
        self.master: tk.Tk = master
        self.manager: TicketManager = manager

        # Configuración de la ventana principal
        self.master.title("DataDesk - Sistema de Gestión de Tickets Helpdesk")
        self.master.geometry("1000x650")
        self.master.minsize(850, 550)

        # Muestra el contenedor principal (relleno X,Y márgenes)
        self.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Inicialización de componentes visuales
        self._create_widgets()
        self.refresh_table()
        self.update_metrics()

    # ==================================================
    # ESTRUCTURA DE LA INTERFAZ Y CREACIÓN DE PANELES
    # ==================================================

    def _create_widgets(self) -> None:
        """
        Crea y distribuye los tres bloques principales de la interfaz.
        1. Panel superior de métricas.
        2. Panel izquierdo con el formulario de registro.
        3. Panel derecho con la tabla, buscador y acciones.
        """
        # *** 1. PANEL SUPERIOR DE MÉTRICAS ***
        self.metrics_frame = ttk.LabelFrame(self, text=" Métricas del Sistema ", padding=10)
        self.metrics_frame.pack(fill=tk.X, pady=(0, 10))

        # Variables para actualizar textos de métricas en tiempo real
        self.lbl_total_var = tk.StringVar(value="Total Tickets: 0")
        self.lbl_pending_var = tk.StringVar(value="Pendientes: 0")
        self.lbl_resolved_var = tk.StringVar(value="Resueltos: 0")

        # Etiquetas de métricas organizadas en columnas
        lbl_total = ttk.Label(self.metrics_frame, textvariable=self.lbl_total_var, font=("Arial", 11, "bold"))
        lbl_total.pack(side=tk.LEFT, expand=True)

        lbl_pending = ttk.Label(self.metrics_frame, textvariable=self.lbl_pending_var, font=("Arial", 11, "bold"), foreground="#D32F2F")
        lbl_pending.pack(side=tk.LEFT, expand=True)

        lbl_resolved = ttk.Label(self.metrics_frame, textvariable=self.lbl_resolved_var, font=("Arial", 11, "bold"), foreground="#388E3C")
        lbl_resolved.pack(side=tk.LEFT, expand=True)

        # Contenedor central dividido en 2 columnas (Formulario a la izquierda, Tabla a la derecha)
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # *** 2. PANEL IZQUIERDO: FORMULARIO DE ENTRADA ***
        self._create_form_panel()

        # *** 3. PANEL DERECHO: BUSCADOR Y TABLA INTERACTIVA ***
        self._create_table_panel()

    def _create_form_panel(self) -> None:
        """
        Construye el panel de formulario (grupo de controles) para dar de alta nuevos tickets.
        """
        # Crea el formulario de registro
        form_frame = ttk.LabelFrame(self.main_container, text=" Registrar Nueva Incidencia ", padding=15)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Campo: Usuario
        ttk.Label(form_frame, text="Usuario / Empleado:").pack(anchor=tk.W, pady=(0, 2))
        self.ent_user = ttk.Entry(form_frame, width=30)
        self.ent_user.pack(fill=tk.X, pady=(0, 10))

        # Campo: Categoría (Combobox)
        ttk.Label(form_frame, text="Categoría:").pack(anchor=tk.W, pady=(0, 2))
        self.cmb_category = ttk.Combobox(
            form_frame,
            values=["Hardware", "Software", "Redes/Conectividad", "Accesos/Permisos", "Soporte General"],
            state="readonly"
        )
        self.cmb_category.current(0)
        self.cmb_category.pack(fill=tk.X, pady=(0, 10))

        # Campo: Prioridad (Combobox)
        ttk.Label(form_frame, text="Prioridad:").pack(anchor=tk.W, pady=(0, 2))
        self.cmb_priority = ttk.Combobox(
            form_frame,
            values=["Baja", "Media", "Alta", "Crítica"],
            state="readonly"
        )
        self.cmb_priority.current(1)
        self.cmb_priority.pack(fill=tk.X, pady=(0, 10))

        # Campo: Descripción
        ttk.Label(form_frame, text="Descripción del Problema:").pack(anchor=tk.W, pady=(0, 2))
        self.txt_description = tk.Text(form_frame, width=28, height=6, font=("Arial", 9))
        self.txt_description.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Botón Guardar Ticket
        btn_save = ttk.Button(form_frame, text="Guardar Ticket", command=self.on_save_ticket)
        btn_save.pack(fill=tk.X)

    def _create_table_panel(self) -> None:
        """
        Construye el panel derecho con el filtro y la tabla Treeview.
        """
        # Crea el panel de consulta
        table_frame = ttk.LabelFrame(self.main_container, text=" Incidencias Registradas ", padding=10)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Barra de búsqueda
        search_frame = ttk.Frame(table_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(search_frame, text="Buscar: ").pack(side=tk.LEFT)
        # Campo para realizar búsquedas
        self.ent_search = ttk.Entry(search_frame)
        self.ent_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        # Evento <KeyRelease>: Filtra automáticamente al presionar cada tecla
        self.ent_search.bind("<KeyRelease>", self.on_search_key_release)

        # Tabla Treeview -> Define las columnas de la tabla
        columns = ("id", "user", "category", "priority", "status", "description")
        # Crea la tabla de tickets
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        # Encabezados o títulos de columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("user", text="Usuario")
        self.tree.heading("category", text="Categoría")
        self.tree.heading("priority", text="Prioridad")
        self.tree.heading("status", text="Estado")
        self.tree.heading("description", text="Descripción")

        # Ancho de columnas
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("user", width=120)
        self.tree.column("category", width=100)
        self.tree.column("priority", width=80, anchor=tk.CENTER)
        self.tree.column("status", width=90, anchor=tk.CENTER)
        self.tree.column("description", width=220)

        # Barra de desplazamiento vertical (Scrollbar)
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Ajusta el tamaño de la tabla en la ventana
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Panel de botones de acción
        action_frame = ttk.Frame(table_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))

        # Botón para cambiar el estado
        btn_resolve = ttk.Button(action_frame, text="Marcar como Resuelto", command=self.on_resolve_ticket)
        btn_resolve.pack(side=tk.LEFT, padx=(0, 10))

        # Botón para eliminar un ticket
        btn_delete = ttk.Button(action_frame, text="Eliminar Ticket", command=self.on_delete_ticket)
        btn_delete.pack(side=tk.LEFT)

    # ==================================================
    # LÓGICA DE EVENTOS Y ACTUALIZACIÓN DE LA INTERFAZ
    # ==================================================

    def update_metrics(self) -> None:
        """
        Recalcula las métricas desde el TicketManager y actualiza las etiquetas del panel superior.
        """
        # Obtiene las métricas actuales
        metrics = self.manager.get_metrics()
        # Actualiza las etiquetas del panel
        self.lbl_total_var.set(f"Total Tickets: {metrics['total']}")
        self.lbl_pending_var.set(f"Pendientes: {metrics['pending']}")
        self.lbl_resolved_var.set(f"Resueltos: {metrics['resolved']}")

    def refresh_table(self, ticket_list: Optional[list] = None) -> None:
        """
        Limpia y vuelve a poblar las filas de la tabla Treeview.

        Args:
            ticket_list (Optional[list]): Lista específica a mostrar. Si es None, muestra todos.
        """
        # Elimina filas existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Si no recibe una lista específica, muestra todos los tickets
        if ticket_list is None:
            ticket_list = self.manager.get_all_tickets()

        # Agrega nuevamente los registros a la tabla
        for ticket in ticket_list:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    ticket.ticket_id,
                    ticket.user_name,
                    ticket.category,
                    ticket.priority,
                    ticket.status,
                    ticket.description
                )
            )

    def _clear_form(self) -> None:
        """
        Limpia las entradas del formulario tras un registro exitoso.
        """
        # Vacía todos los campos del formulario
        self.ent_user.delete(0, tk.END)
        self.cmb_category.current(0)
        self.cmb_priority.current(1)
        self.txt_description.delete("1.0", tk.END)

    # ==================================================
    # CONTROLADORES DE EVENTOS (BOTONES Y BÚSQUEDA)
    # ==================================================

    def on_save_ticket(self) -> None:
        """
        Maneja el evento de guardar un nuevo ticket. Valida los datos e informa al usuario.
        """
        # Obtiene la información del formulario
        user = self.ent_user.get().strip()
        category = self.cmb_category.get()
        priority = self.cmb_priority.get()
        description = self.txt_description.get("1.0", tk.END).strip()

        # Validación simple de datos obligatorios
        if not user or not description:
            messagebox.showwarning("Campos Incompletos",
                                   "Por favor, completa el usuario y la descripción del problema.")
            return

        # Crear ticket usando el TicketManager
        self.manager.create_ticket(
            user_name=user,
            description=description,
            category=category,
            priority=priority
        )

        # Informa que el registro fue exitoso
        messagebox.showinfo("Éxito", "El ticket ha sido registrado correctamente.")

        # Actualiza la interfaz
        self._clear_form()
        self.refresh_table()
        self.update_metrics()

    def on_search_key_release(self, event: tk.Event) -> None:
        """
        Filtra dinámicamente la tabla al escribir en el cuadro de búsqueda.
        """
        # Obtiene el texto de búsqueda
        query = self.ent_search.get()

        # Busca los tickets que coinciden
        filtered_tickets = self.manager.search_tickets(query)
        self.refresh_table(filtered_tickets)

    def _get_selected_ticket_id(self) -> Optional[int]:
        """
        Obtiene el ID del ticket seleccionado en la tabla Treeview.

        Returns:
            Optional[int]: El ID del ticket o None si no hay selección.
        """
        # Obtiene la fila seleccionada
        selected_item = self.tree.selection()

        # Verifica que exista una selección
        if not selected_item:
            messagebox.showwarning("Selección Requerida", "Por favor, selecciona un ticket de la tabla.")
            return None

        # Obtener los valores de la fila seleccionada
        values = self.tree.item(selected_item[0], "values")
        return int(values[0])

    def on_resolve_ticket(self) -> None:
        """
        Cambia el estado del ticket seleccionado a 'Resuelto'.
        """
        # Obtiene el ticket seleccionado
        ticket_id = self._get_selected_ticket_id()

        # Actualiza el estado del ticket
        if ticket_id is not None:
            if self.manager.update_status(ticket_id, "Resuelto"):
                messagebox.showinfo("Ticket Actualizado", f"El ticket #{ticket_id} ha sido marcado como Resuelto.")

                # Refresca la información en pantalla
                self.refresh_table()
                self.update_metrics()

    def on_delete_ticket(self) -> None:
        """
        Solicita confirmación mediante messagebox y elimina el ticket seleccionado.
        """
        # Obtiene el ticket seleccionado
        ticket_id = self._get_selected_ticket_id()
        if ticket_id is not None:

            # Solicita confirmación antes de eliminar
            confirm = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Estás seguro de que deseas eliminar el ticket #{ticket_id}?\nEsta acción no se puede deshacer."
            )
            # Elimina el ticket si el usuario confirma
            if confirm:
                if self.manager.delete_ticket(ticket_id):
                    messagebox.showinfo("Ticket Eliminado", f"El ticket #{ticket_id} ha sido eliminado con éxito.")

                    # Actualiza la tabla y las métricas
                    self.refresh_table()
                    self.update_metrics()