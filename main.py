# ==============================================================================
# MÓDULO: main.py
# Punto de Entrada Principal de la Aplicación DataDesk
# ==============================================================================

import tkinter as tk
from models import TicketManager
from views import HelpdeskView

def main() -> None:
    """
    Función principal encargada de inicializar la ventana raíz de Tkinter,
    instanciar las capas del sistema (Modelo y Vista) y ejecutar el bucle principal.
    """
    try:
        # Inicialización del entorno gráfico principal de Tkinter
        root = tk.Tk()

        # Instancia del gestor de datos (Bakend/model) | Capa de Lógica y Persistencia
        manager = TicketManager(file_path="tickets.json")

        # Instancia de la interfaz de usuario (Capa de Vista)
        app = HelpdeskView(master=root, manager=manager)

        # Ejecución del bucle principal de eventos de la GUI (metodo mainloop de Tkinter)
        root.mainloop()

    except Exception as error:
        print(f"Ocurrió un error inesperado al iniciar la aplicación: {error}")

# **************************************************
# BLOQUE DE EJECUCIÓN INICIAL
# **************************************************
if __name__ == "__main__":
    main()