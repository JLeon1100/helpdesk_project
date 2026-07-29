# ==============================================================================
# MÓDULO: main.py
# Punto de Entrada Principal de la Aplicación DataDesk
# ==============================================================================

import tkinter as tk # Importa la librería para crear la interfaz gráfica
from models import TicketManager # Importa el gestor de tickets
from views import HelpdeskView # Importa la ventana principal

def main() -> None:
    """
    Función principal encargada de inicializar la ventana raíz de Tkinter,
    instanciar las capas del sistema (Modelo y Vista) y ejecutar el bucle principal.
    """
    try:
        # Inicialización del entorno gráfico principal de Tkinter
        # Crea la ventana principal
        root = tk.Tk()

        # Instancia del gestor de datos (Bakend/model) | Capa de Lógica y Persistencia
        # Carga el archivo con los tickets
        manager = TicketManager(file_path="tickets.json")

        # Instancia de la interfaz de usuario (Capa de Vista)
        # Conecta la vista con el modelo
        app = HelpdeskView(master=root, manager=manager)

        # Ejecución del bucle principal de eventos de la GUI (metodo mainloop de Tkinter)
        # Mantiene la aplicación en ejecución
        root.mainloop()

    except Exception as error:
        # Muestra cualquier error al iniciar
        print(f"Ocurrió un error inesperado al iniciar la aplicación: {error}")

# **************************************************
# BLOQUE DE EJECUCIÓN INICIAL
# **************************************************

# Ejecuta la aplicación solo si este archivo es el principal
if __name__ == "__main__":
    main()