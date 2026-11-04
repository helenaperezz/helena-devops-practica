# ENTRADA DE LA APLICACION: se definen los endpoints de la API REST (para activarlo ejecutar pip install -r requirements.txt y uvicorn main:app --reload)

#Bibliotecas y modulos
from typing import Dict, List  

from fastapi import FastAPI, HTTPException, status  # FastAPI = la aplicación, HTTPException = errores HTTP, status = códigos HTTP con nombre

from models.pedido import Pedido 
from models.producto import Producto, ProductoElectronico, ProductoRopa  
from schemas import (  
    PedidoCreate,  
    PedidoItemRead, 
    PedidoRead, 
    ProductoCreate,  
    ProductoRead,  
    UsuarioCreate,  
    UsuarioRead,
)
from services.Tienda_service import TiendaService

app = FastAPI(title="Tienda online", description="API REST de la tienda online de Helena (Práctica 2)", version="1.0")  # creamos la aplicación; título y descripción salen en /docs

tienda = TiendaService()  # única instancia del servicio; guarda usuarios, productos y pedidos en memoria

# FUNCIONES AUXILIARES

def producto_a_read(producto: Producto) -> ProductoRead:  # convierte un Producto (genérico, electrónico o ropa) en ProductoRead
    if isinstance(producto, ProductoElectronico):  # si el objeto es un producto electrónico
        tipo = "electronico"  
    elif isinstance(producto, ProductoRopa):  # si el objeto es una prenda de ropa
        tipo = "ropa"  
    else:  # en cualquier otro caso es un producto genérico
        tipo = "generico"  
    return ProductoRead(  #esquema de salida
        id=producto.id,  # copiamos el id
        tipo=tipo,  # tipo que hemos calculado arriba
        nombre=producto.nombre,  # copiamos el nombre
        precio=producto.precio,  # copiamos el precio
        stock=producto.stock,  # copiamos el stock
        meses_garantia=getattr(producto, "meses_garantia", None),  #devuelve None si el producto no tiene ese atributo
        talla=getattr(producto, "talla", None), 
        color=getattr(producto, "color", None),  
    )


def pedido_a_read(pedido: Pedido) -> PedidoRead:  # convierte un Pedido en PedidoRead
    items = [  # creamos la lista de líneas del pedido
        PedidoItemRead(  # una línea por cada producto del pedido
            producto_id=producto.id, 
            nombre=producto.nombre, 
            precio_unitario=producto.precio,  
            cantidad=cantidad,  
            subtotal=round(producto.precio * cantidad, 2),  # precio por cantidad, redondeado a 2 decimales
        )
        for producto, cantidad in pedido.productos  
    ]
    return PedidoRead(  #esquema de salida
        id=pedido.id, 
        fecha=pedido.fecha,  
        cliente_id=pedido.cliente.id,  
        cliente_nombre=pedido.cliente.nombre, 
        total=round(pedido.total, 2), 
        items=items,  # líneas que hemos creado arriba
    )
    
# ENDPOINTS DE USUARIOS

@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)  # POST /usuarios: crea un usuario y responde 201 (Created)
def crear_usuario(datos: UsuarioCreate):  # FastAPI valida el cuerpo de la petición con UsuarioCreate
    try:  # intentamos crear el usuario
        usuario = tienda.registrar_usuario(datos.tipo, datos.nombre, datos.email, datos.direccion)  # usamos la lógica de TiendaService
    except ValueError as error:  # si el servicio rechaza los datos
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))  # respondemos 400 con el mensaje del error
    return UsuarioRead(id=usuario.id, nombre=usuario.nombre, email=usuario.email, es_admin=usuario.is_admin())# devolvemos el usuario creado en formato UsuarioRead


@app.get("/usuarios", response_model=List[UsuarioRead])  # GET /usuarios: lista de todos los usuarios
def listar_usuarios():  # no necesita parámetros
    return [UsuarioRead(id=usuario.id, nombre=usuario.nombre, email=usuario.email, es_admin=usuario.is_admin()) for usuario in tienda.listar_usuarios()]  


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)  # GET /usuarios/{usuario_id}: devuelve un usuario concreto
def obtener_usuario(usuario_id: str):  # el id llega en la URL
    usuario = tienda.obtener_usuario(usuario_id)  # buscamos el usuario en el servicio
    if usuario is None:  # si no existe
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ningún usuario con id {usuario_id}.")  # error 404
    return UsuarioRead(id=usuario.id, nombre=usuario.nombre, email=usuario.email, es_admin=usuario.is_admin()) # devolvemos el usuario en formato UsuarioRead

# ENDPOINTS DE PRODUCTOS

@app.post("/productos", response_model=ProductoRead, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)  # POST /productos: crea un producto; exclude_none oculta los atributos que no aplican al tipo
def crear_producto(datos: ProductoCreate): 
    try: 
        producto = tienda.añadir_productos(  
            datos.tipo,  
            datos.nombre, 
            datos.precio, 
            datos.stock,  # stock inicial
            meses_garantia=datos.meses_garantia,  # garantía (solo electrónicos)
            talla=datos.talla,  # talla (solo ropa)
            color=datos.color,  # color (solo ropa)
        )
    except ValueError as error:  # si el servicio rechaza los datos
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))  # respondemos 400 con el mensaje del error
    return producto_a_read(producto)  # devolvemos el producto creado en formato ProductoRead


@app.get("/productos", response_model=List[ProductoRead], response_model_exclude_none=True)  # GET /productos: lista de todos los productos
def listar_productos(): 
    return [producto_a_read(producto) for producto in tienda.listar_productos()]  


@app.get("/productos/{producto_id}", response_model=ProductoRead, response_model_exclude_none=True)  # GET /productos/{producto_id}: devuelve un producto concreto
def obtener_producto(producto_id: str):  # el id llega en la URL
    producto = tienda.obtener_producto(producto_id)  
    if producto is None:  # si no existe
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ningún producto con id {producto_id}.")  # error 404
    return producto_a_read(producto)  # devolvemos el producto en formato ProductoRead


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)  # DELETE /productos/{producto_id}: elimina un producto; 204 = hecho, sin contenido que devolver
def eliminar_producto(producto_id: str):  # el id llega en la URL
    try:  
        tienda.eliminar_productos(producto_id) 
    except ValueError as error:  # el servicio lanza ValueError si el producto no existe
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))  # respondemos 404 con el mensaje del error
    
# ENDPOINTS DE PEDIDOS

@app.post("/pedidos", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)  # POST /pedidos: crea un pedido y responde 201 (Created)
def crear_pedido(datos: PedidoCreate):  # FastAPI valida el cuerpo de la petición con PedidoCreate
    if tienda.obtener_usuario(datos.cliente_id) is None:  # comprobamos que el cliente existe
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ningún usuario con id {datos.cliente_id}.")  # error 404

    cantidades: Dict[str, int] = {}  # diccionario {id_producto: cantidad total}; así unimos líneas repetidas del mismo producto
    for item in datos.items: 
        cantidades[item.producto_id] = cantidades.get(item.producto_id, 0) + item.cantidad  # sumamos la cantidad al producto (0 si es la primera vez)

    for producto_id in cantidades:  # recorremos los productos distintos del pedido
        if tienda.obtener_producto(producto_id) is None:  # comprobamos que el producto existe
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ningún producto con id {producto_id}.")  # error 404

    lineas = list(cantidades.items())  # lista de tuplas (id_producto, cantidad), el formato que espera TiendaService

    try: 
        pedido = tienda.realizar_pedido(datos.cliente_id, lineas)  # el servicio comprueba el stock y que el usuario sea cliente
    except ValueError as error:  # por ejemplo: stock insuficiente o usuario administrador
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))  # respondemos 400 con el mensaje del error
    return pedido_a_read(pedido)  # devolvemos el pedido creado en formato PedidoRead


@app.get("/usuarios/{cliente_id}/pedidos", response_model=List[PedidoRead])  # GET /usuarios/{cliente_id}/pedidos: historial de pedidos de un cliente
def listar_pedidos_cliente(cliente_id: str):  # el id del cliente llega en la URL
    if tienda.obtener_usuario(cliente_id) is None:  # comprobamos que el cliente existe
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ningún usuario con id {cliente_id}.")  # error 404
    return [pedido_a_read(pedido) for pedido in tienda.listar_pedidos_usuarios(cliente_id)]  # convertimos cada pedido (lista vacía si no tiene)


