from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    """
    Modelo para requisições de criação de usuário.

    Attributes:
        username (str): Nome de usuário.
        password (str): Senha do usuário.
    """
    username: str
    password: str
