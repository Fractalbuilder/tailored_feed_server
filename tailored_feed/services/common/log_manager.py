import logging
from datetime import datetime
from .exception_manager import ExceptionManager

class LogManager:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger('django')
        self.exception_manager = ExceptionManager()

    def log_report(self, method_name: str, parameters: dict=None, trace=""):
        """
        Escribe el reporte de una excepción en el log de errores en un formato estándar.

        Recibe:
            Argumentos:
                method_name (str): <Nombre del método donde se produce la excepción>,
                parameters (dict): <Argumentos del metodo donde se produce la excepción>,
                exception_trace (str): <Información de excepción anterior>
        
        Autor:
            Nombre: Jaime Andrés García
            Correo: jaime.garcia@makrosoft.co
        """
        
        exception_string = self.exception_manager.format(method_name, parameters, trace)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logger.error(" [ " + current_time + " ] " + exception_string + "\n")