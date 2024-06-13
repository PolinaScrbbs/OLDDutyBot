import re

class RegistrationValidationError(Exception):
    pass

class RegistrationValidator:
    def __init__(self, full_name: str, password: str, confirm_password: str) -> None:
        self.full_name = full_name
        self.password = password
        self.confirm_password = confirm_password

    async def validate(self):
        try:
            await self.validate_full_name(self.full_name)
            await self.validate_password(self.password)
        except RegistrationValidationError as e:
            return str(e)

    async def validate_full_name(self, full_name: str):
        if not self.full_name:
            raise RegistrationValidationError("ФИО не может быть пустым")
        if not re.match(r"^[а-яА-ЯёЁ]+\s[а-яА-ЯёЁ]+\s[а-яА-ЯёЁ]+$", full_name):
            raise RegistrationValidationError("Полное имя должно состоять из трех слов, записанных только русскими буквами")

    async def validate_password(self, password: str):
        if not self.full_name:
            raise RegistrationValidationError("Пароль не может быть пустым")
        if self.password != self.confirm_password:
            raise RegistrationValidationError("Пароли не совпадают")
        elif len(password) < 8:
            raise RegistrationValidationError("Длина пароля должна составлять не менее 8 символов.")
        elif len(password) > 20:
            raise RegistrationValidationError("Длина пароля не может быть более 20 символов.")
        elif not re.search(r"^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};:'\\|,.<>\/?]*$", password):
            raise RegistrationValidationError("Пароль должен состоять только из латинских букв, цифр и специальных символов.")
        elif not re.search("[a-z]", self.password):
            raise RegistrationValidationError("Пароль должен содержать хотя бы одну строчную букву.")
        elif not re.search("[A-Z]", self.password):
            raise RegistrationValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
        elif not re.search("[0-9]", self.password):
            raise RegistrationValidationError("Пароль должен содержать хотя бы одну цифру.")
        elif not re.search("[!@#$%^&*()_+-=]", self.password):
            raise RegistrationValidationError("Пароль должен содержать хотя бы один специальный символ.")
