import json

class ExceptionManager:

    def throw_report(self, failed_object: object, method_name: str, parameters=None, exception_trace: str =""):
        """
        Genera una excepción en un formato estándar, que indica el método y argumentos de un bloque de 
        código donde ocurrió una excepción.

        Recibe:
            Argumentos:
                failed_(object): <Objeto que produce la excepción>
                method_name (str): <Nombre del método>,
                parameters (dict): <Nombre y metodo donde se produce la excepción>,
                exception_trace (str): <Información de excepción anterior>

        Excepciones:
            Exception: Si se encuentran excepciones no controladas
        
        Autor:
            Nombre: Jaime Andrés García
            Correo: jaime.garcia@makrosoft.co
        """

        class_location = f"{failed_object.__class__.__module__}.{failed_object.__class__.__name__}"
        method_path = class_location + "." + method_name
        exception_string = self.format(method_path, parameters, exception_trace)

        raise Exception(exception_string)

    def format(self, method_name: str, parameters: dict=None, exception_trace: str=""):
        """
        Genera una cadena en un formato estándar, que indica el método y argumentos de un bloque de 
        código donde ocurre una excepción.

        Recibe:
            Argumentos:
                method_name (str): <Nombre del método donde se produce la excepción>,
                parameters (dict): <Argumentos del metodo donde se produce la excepción>,
                exception_trace (str): <Información de excepción anterior>

        Retorna:
            Cadena estandarizada con reporte de excepción.

        Autor:
            Nombre: Jaime Andrés García
            Correo: jaime.garcia@makrosoft.co
        """

        if parameters is None:
            parameters = {}

        for key, value in parameters.items():
            if hasattr(value, '__class__') and value is not None and not isinstance(value, (int, float, str, bool)):
                class_location = f"{value.__class__.__module__}.{value.__class__.__name__}"
                parameters[key] = class_location
    
        context = {
            'method': method_name,
            'parameters': parameters
        }

        return f"{exception_trace} {json.dumps(context)}"