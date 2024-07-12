from pydantic import BaseModel


class KeyDTO(BaseModel):
    key: str
    name: str


class BitArrayDTO(BaseModel):
    bitarray: str
    key_name: str
