import inspect
from django.db import transaction
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.repositories.common.db_repository_interface import DbRepositoryInterface

class DbRepository(DbRepositoryInterface):

    def __init__(self):
        self.exception_manager = ExceptionManager()

    def start_transaction(self):
        """
        Starts a database transaction.

        Autor:
            Nombre: Jaime Andrés García
            Correo: jaime.garcia@makrosoft.co
        """

        try:
            self.transaction = transaction.atomic()
            self.transaction.__enter__()

        except Exception as e:
            argspec = inspect.getfullargspec(self.start_transaction)
            parametros = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "start_transaction", parametros, str(e))

    def save(self):
        """
        Commits the transaction to the database.

        Autor:
            Nombre: Jaime Andrés García
            Correo: jaime.garcia@makrosoft.co
        """

        try:
            self.transaction.__exit__(None, None, None)

        except Exception as e:
            argspec = inspect.getfullargspec(self.save)
            parametros = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "save", parametros, str(e))

    def roll_back(self):
        """
        Rolls back the transaction, discarding changes.

        Autor:
            Nombre: Jaime Andrés García
            Correo: jaime.garcia@makrosoft.co
        """

        try:
            transaction.set_rollback(True)

        except Exception as e:
            argspec = inspect.getfullargspec(self.roll_back)
            parametros = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "roll_back", parametros, str(e))


    def close_transaction(self):
        """
        Closes the transaction and ensures cleanup.

        Autor:
            Nombre: Jaime Andrés García
            Correo: jaime.garcia@makrosoft.co
        """

        try:
            if hasattr(self, 'transaction'):
                self.transaction.__exit__(None, None, None)

        except Exception as e:
            argspec = inspect.getfullargspec(self.close_transaction)
            parametros = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "close_transaction", parametros, str(e))