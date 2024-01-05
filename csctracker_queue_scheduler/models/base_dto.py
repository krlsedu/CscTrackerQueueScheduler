class BaseDTO:
    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if value is None or (isinstance(value, list) and not value):  # Ignore None and empty lists
                continue
            if callable(value):  # Ignore functions/methods
                continue
            if hasattr(value, 'to_dict'):  # If value has to_dict method, call it
                result[key] = value.to_dict()
            elif isinstance(value, list):  # If value is a list, call to_dict on its items if possible
                result[key] = [item.to_dict() if hasattr(item, 'to_dict') else item for item in value]
            else:  # Otherwise, just assign value
                result[key] = value
        return result

    def update(self, param):
        if isinstance(param, dict):
            attr_dict = param
        else:
            self.data: list = [param]
            return

        for key, value in attr_dict.items():
            setattr(self, key, value)
