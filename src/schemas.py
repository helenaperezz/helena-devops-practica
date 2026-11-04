# ARCHIVOS CON ESQUEMA PYDANTIC
# esquemas create:validan lo que envia el cliente. Esquemas read: definen lo que se devuelve


# Modulos y bibliotecas
from datetime import datetime 
from typing import List, Literal, Optional  

from pydantic import BaseModel, ConfigDict, Field, model_validator 

# ESQUEMAS DE USUARIOS

class UsuarioCreate(BaseModel):  # datos que envía el cliente para crear un usuario
    model_config = ConfigDict(str_strip_whitespace=True)  # quita los espacios sobrantes de los textos, así "   " cuenta como vacío y se rechaza
    nombre: str = Field(min_length=1)  # nombre obligatorio y que no esté vacío
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")  # email obligatorio con formato válido (algo@algo.algo)
    tipo: Literal["cliente", "administrador"]  #solo se admiten estos dos tipos de usuario
    direccion: Optional[str] = None  # dirección postal: opcional en general, obligatoria si es cliente (se comprueba abajo)

    @model_validator(mode="after")  # se ejecuta cuando ya se han validado todos los campos
    def validar_direccion(self) -> "UsuarioCreate":  # comprueba la regla que depende de dos campos (tipo y dirección)
        if self.tipo == "cliente" and not self.direccion:  # si es cliente y no ha mandado dirección (o está vacía)
            raise ValueError("Un cliente necesita una dirección postal.")  # FastAPI responderá automáticamente con error 422
        return self  # si todo está bien, devolvemos el objeto validado


class UsuarioRead(BaseModel):  # datos que devolvemos al cliente sobre un usuario
    id: str  # identificador único (uuid) del usuario
    nombre: str  # nombre del usuario
    email: str  # email del usuario
    es_admin: bool  # True si es administrador, False si es cliente
    
# ESQUEMAS DE PRODUCTOS

class ProductoCreate(BaseModel):  # datos que envía el cliente para crear un producto.
    model_config = ConfigDict(str_strip_whitespace=True)  # quita los espacios sobrantes de los textos (nombre, talla, color)
    tipo: Literal["generico", "electronico", "ropa"]  # solo se admiten estos tres tipos de producto
    nombre: str = Field(min_length=1)  # nombre obligatorio y que no este vacío
    precio: float = Field(gt=0)  # el precio debe ser mayor que 0
    stock: int = Field(ge=0)  # el stock debe ser 0 o más (nunca negativo)
    meses_garantia: Optional[int] = Field(default=None, ge=0)  # solo paa electrónicos (si se envía, no puede ser negativo)
    talla: Optional[str] = None  # solo para ropa
    color: Optional[str] = None  # solo para ropa

    @model_validator(mode="after")  # se ejecuta cuando ya se han validado todos los campos
    def validar_atributos_segun_tipo(self) -> "ProductoCreate":  # comprueba que estén los atributos que exige cada tipo
        if self.tipo == "electronico" and self.meses_garantia is None:  
            raise ValueError("Un producto electrónico necesita meses_garantia.")  # error 422 automático
        if self.tipo == "ropa" and (not self.talla or not self.color):  
            raise ValueError("Un producto de ropa necesita talla y color.")  # error 422 automático
        return self  # si todo está bien, devolvemos el objeto validado


class ProductoRead(BaseModel):  # datos que devolvemos al cliente sobre un producto
    id: str  #identificador único (uuid) del producto
    tipo: str  # "generico", "electronico" o "ropa"
    nombre: str 
    precio: float  
    stock: int  # unidades disponibles
    meses_garantia: Optional[int] = None  # solo aparece si es electrónico
    talla: Optional[str] = None  # solo aparece si es ropa
    color: Optional[str] = None  # solo aparece sies ropa
    
# ESQUEMAS DE PEDIDOS

class PedidoItemCreate(BaseModel):  
    producto_id: str  # id del producto que se quiere comprar
    cantidad: int = Field(gt=0)  # la cantidad debe ser al menos 1


class PedidoCreate(BaseModel):  # datos que envía el cliente para crear un pedido
    cliente_id: str  # id del cliente que hace el pedido
    items: List[PedidoItemCreate] = Field(min_length=1)  


class PedidoItemRead(BaseModel):  
    producto_id: str 
    nombre: str 
    precio_unitario: float  # precio de una unidad
    cantidad: int  
    subtotal: float  # precio_unitario * cantidad


class PedidoRead(BaseModel):  
    id: str  # identificador único (uuid) del pedido
    fecha: datetime  # fecha y hora en la que se hizo el pedido
    cliente_id: str  #id del cliente que lo hizo
    cliente_nombre: str  # nombre del cliente que lo hizo
    total: float  # importe total del pedido
    items: List[PedidoItemRead]  # líneas del pedido

