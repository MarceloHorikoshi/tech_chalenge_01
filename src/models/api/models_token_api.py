from pydantic import BaseModel


class Token(BaseModel):
    """
    Modelo para representar um token de acesso.

    Attributes:
        access_token (str): O token de acesso.
        token_type (str): O tipo de token (e.g., "bearer").
    """

    access_token: str
    token_type: str
