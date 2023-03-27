from rest_framework.exceptions import ParseError


class Time15MinutesValidator:
    message = 'Время должно быть кратно 15 минутам.'

    def __call__(self, value):  # при вызове валидатора
        if not value:
            return
        if value.minute % 15 > 0:
            return ParseError(self.message)