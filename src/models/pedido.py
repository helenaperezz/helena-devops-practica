# ARCHIVO CON CLASE PEDIDO QUE SE VINCULA A UN USUARIO Y A UNA LISTA DE PRODUCTOS CON SUS CANTIDADES CORRESPONDIENTES

# importacion librerias y clases
import uuid
from datetime import datetime
from typing import List, Tuple

from models.producto import Producto
from models.usuario import Cliente

# Clase Pedido
class Pedido:
    def __init__(self, cliente: Cliente, productos: List[Tuple[Producto, int]]):
        self.id = str(uuid.uuid4())  # Genera un identificador único aleatorio. Se convierte a str para facilitar su uso.
        self.cliente = cliente  # objeto de la clase Usuario (Cliente)
        self.productos = productos  # lista de tuplas (producto, cantidad)
        
        self.fecha = datetime.now()  # fecha y hora en la que se hace el pedido
        self.total = self.calcular_total()  # importe total del pedido

    def calcular_total(self) -> float:
    #Calcula el importe total del pedido sumando (precio * cantidad) de cada producto incluido en el pedido.
        total = 0.0
        
        for producto, cantidad in self.productos: # Recorre la lista de productos y sus cantidades
            total += producto.precio * cantidad #suma el precio del producto multiplicado por la cantidad al total
        return total

    def __str__(self):
    #Devuelve un resumen del pedido: cliente, fecha, productos incluidos y el total de la compra.
        # Construimos un listado de "nombre x cantidad" para cada producto.
        detalle_productos = ", ".join(f"{producto.nombre} x{cantidad}" for producto, cantidad in self.productos)
        
        #strftime para formatear la fecha en un formato legible
        fecha_legible = self.fecha.strftime("%d/%m/%Y %H:%M")
        
        #devuelve la informacion del pedido (id, nombre del cliente, fecha, productos y total)
        return f"Pedido(id={self.id}, cliente={self.cliente.nombre}, fecha={fecha_legible}, productos=[{detalle_productos}], total={self.total})"


