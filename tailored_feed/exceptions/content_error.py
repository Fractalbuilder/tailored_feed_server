class ContentError(Exception):
    def __init__(self, message="Bad Request", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)