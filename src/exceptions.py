class BadInput(Exception):

    def __init__(self, parameter_name: str, parameter_value) -> None:
        self.message = f"Parameter '{parameter_name}' cannot have '{parameter_value}' for value"
        super().__init__(self.message)
