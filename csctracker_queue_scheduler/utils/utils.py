import re


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def snake_to_camel(word):
        split_word = re.split('_', word)
        return ''.join(x.capitalize() for x in split_word)

    @staticmethod
    def camel_to_snake(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def to_snake_case(str_, scream):
        if str_ is None:
            return None
        str_ = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str_)
        str_ = re.sub('([a-z0-9])([A-Z])', r'\1_\2', str_).lower()
        str_ = str_.replace(" ", "_")
        if scream:
            str_ = str_.upper()
        return str_

    @staticmethod
    def get_friendly_method_name(method_name):
        try:
            try:
                function_class = method_name.__self__.__class__.__name__
            except:
                function_class = method_name.__class__.__name__
            function_name = method_name.__name__
            return f"{function_class}.{function_name}"
        except:
            return method_name
