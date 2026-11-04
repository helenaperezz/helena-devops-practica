# ARCHIVO CON CLASE TIENDASERVICE (intermediario entre usuarios y productos)

#librerias y clases importadas
from typing import Dict, List, Optional, Tuple
 
from models.usuario import Usuario,Cliente, Administrador
from models.producto import Producto, ProductoElectronico, ProductoRopa
from models.pedido import Pedido

class TiendaService:
# servicio central que gestiona usuarios productos y pedidos
    def __init__(self) -> None:
        self.usuarios: Dict[str, Usuario] = {}
        self.productos: Dict[str, Producto] = {}
        self.pedidos: List[Pedido] = []

    #GESTION DE USUARIOS
    def registrar_usuario(
        self,
        tipo: str,
        nombre: str,
        email: str,
        direccion: Optional[str] = None, #solo necesario si tipo es "cliente"
    ) -> Usuario:
#registra un nuevo usuario en la tienda
# Devuelve Usuario ya creado
        if tipo == "cliente":
            if direccion is None:
                raise ValueError("Un cliente necesita una dirección postal.")
            usuario: Usuario = Cliente(nombre, email, direccion)
# si el tipo de usuario es administrador no hace falta direccion
        elif tipo == "administrador":
            usuario = Administrador(nombre, email)
        else:
            # por si nos pasan un tipo de usuario que no se reconoce
            raise ValueError(f"Tipo de usuario no soportado: {tipo}")

        #guarda el usuario en el diccionario usando su id como clave.
        self.usuarios[usuario.id] = usuario
        return usuario
    
    # devuelve un usuario concreto por su id, o None si no existe (main.py responde 404 en ese caso)
    def obtener_usuario(self, usuario_id: str) -> Optional[Usuario]:
        return self.usuarios.get(usuario_id)  # .get devuelve None en vez de lanzar error si la clave no existe
    
    # lista con todos los usuarios registrados
    def listar_usuarios(self) -> List[Usuario]:
        return list(self.usuarios.values())  # .values nos da los objetos Usuario del diccionario
    
    #GESTIÓN DE PRODUCTOS
    def añadir_productos(
        self,
        tipo: str,
        nombre: str,
        precio: float,
        stock: int,
        meses_garantia: Optional[int] = None,
        talla: Optional[str] = None,
        color: Optional[str] = None,
    ) -> Producto: # añade el producto al inventario y devuelve el producto
        
        # un producto genérico no necesita atributos extra (el enunciado pide validar los tres tipos: genérico, electrónico y ropa)
        if tipo == "generico":
            producto: Producto = Producto(nombre, precio, stock)
            
        # meses_garantia solo necesario si tipo == electronico, si no error
        elif tipo == "electronico":
            if meses_garantia is None:
                raise ValueError("Un producto electrónico necesita meses_garantía")
            producto = ProductoElectronico (nombre, precio, stock, meses_garantia)
    
        # color y talla solo necesario si tipo == ropa, sino da error
        elif tipo == "ropa":
            if talla is None or color is None:
                raise ValueError("Un producto de ropa necesita talla y color")
            producto= ProductoRopa (nombre, precio, stock, talla, color)
            
        #Si no es ninguna de las categorías anteriores da error
        else:
            raise ValueError(f"Tipo de producto no soportado: {tipo}")
        
        # Guardamos el producto en el diccionario usando su id como clave.
        self.productos[producto.id] = producto
        return producto
    
    # devuelve un producto concreto por su id, o None si no existe (main.py responde 404 en ese caso)
    def obtener_producto(self, producto_id: str) -> Optional[Producto]:
        return self.productos.get(producto_id)  # .get devuelve None en vez de lanzar error si la clave no existe
        
    # elimina un producto del inventario con su identificador
    def eliminar_productos(self, producto_id:str) -> None:
        if producto_id not in self.productos:
            raise ValueError(f"No existe ningún producto con id {producto_id}.")
        del self.productos[producto_id] # borra el elemento del diccionario
        
    # lista con todos los productos de la tienda
    def listar_productos(self) -> List[Producto]:
        return list(self.productos.values()) #.values nos da los objetos Producto del diccionario.
    
    # GESTIÓN DE PEDIDOS 
    def realizar_pedido(
        self, usuario_id: str, lineas_pedido: List[Tuple[str, int]]
    ) -> Pedido: # Realiza un pedido para un usuario
        #lineas_pedidoes una lista de tuplas (id_producto, cantidad)
        
        # Comprobacion de que existe el usuario
        usuario = self.usuarios.get(usuario_id)
        if usuario is None:
            raise ValueError(f"No existe ningún usuario con id {usuario_id}.")
        
        # solo pueden realizar pedidos los clientes, no los administradores
        if not isinstance(usuario, Cliente):
            raise ValueError("Solo un cliente puede realizar pedidos.")
        
        #Comprobamos que haya stock antes de descontarlos para no dejar un pedido a medias si algo falla
        productos_del_pedido: List[Tuple[Producto, int]] = []
        
        for producto_id, cantidad in lineas_pedido:
            producto = self.productos.get(producto_id)
            
            if producto is None: # si no existe ese id
                raise ValueError(f"No existe ningún producto con id {producto_id}.")
            
            if not producto.hay_stock(cantidad): #si no hay suficiente stock
                raise ValueError(
                    f"Stock insuficiente de '{producto.nombre}' "
                    f"(disponible: {producto.stock}, solicitado: {cantidad})."
                )
            
            productos_del_pedido.append((producto, cantidad))
            
        # Como todo es correcto
        pedido = Pedido(usuario, productos_del_pedido)
        
        #descontamos el stock de cada producto
        for producto, cantidad in productos_del_pedido:
            producto.actualizar_stock(-cantidad)
            
        #guardamos el pedido en el histórico general
        self.pedidos.append(pedido)
        
        return pedido  #se devuelve el pedido
    
    def listar_pedidos_usuarios(self,usuario_id:str) -> List[Pedido]:
        #devuelve los pedidos de un usuario por su id con la fecha
        pedidos_usuario =[
            pedido for pedido in self.pedidos if pedido.cliente.id == usuario_id
        ]
        
        return sorted(pedidos_usuario, key=lambda pedido: pedido.fecha)
        #sorted() con key=lambda ordena la lista usando la fecha de cada pedido.
               

