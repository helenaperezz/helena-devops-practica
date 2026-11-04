# ARCHIVO CON CLASE PADRE PRODUCTO Y DOS SUBCLASES PRODUCTOELECTRONICO Y PRODUCTOROPA
# Clase padre: Producto (tiene todo lo común a cualquier producto de la tienda: id, nombre, precio, stock)

#importar biblioteca uuid para generar identificadores únicos automáticamente
import uuid

# Clase padre Producto
class Producto:
    def __init__(self, nombre: str, precio: float, stock: int):
        self.id = str(uuid.uuid4())  # Genera un identificador único aleatorio. Se convierte a str para facilitar su uso.
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def hay_stock(self, cantidad: int) -> bool:
    # Comprueba si hay stock suficiente para una cantidad solicitada, devuelve True si hay suficiente, False si no.
        return self.stock >= cantidad

    def actualizar_stock(self, cantidad: int):
    #actualiza el stock del producto. 
    #-> Si 'cantidad' es negativa -> se están vendiendo unidades (compra). 
    #-> Si 'cantidad' es positiva -> se están añadiendo unidades (reposición).
        nuevo_stock = self.stock + cantidad
        
        #asi evitamos que el stock pueda quedar en negativo por error.
        if nuevo_stock < 0:
            raise ValueError("El stock no puede quedar por debajo de 0.")
        self.stock = nuevo_stock

    def __str__(self):
    #representacion del producto que luego se sobreescribira en las subclases para añadir los atributos propios de cada producto
        return f"Producto(id={self.id}, nombre={self.nombre}, precio={self.precio}, stock={self.stock})"
    
#subclase ProductoElectronico que hereda de Producto y añade el atributo meses_garantia
class ProductoElectronico(Producto):
    def __init__(self, nombre: str, precio: float, stock: int, garantia: int):
        super().__init__(nombre, precio, stock) #llamamos al constructor de la clase padre para inicializar id, nombre, precio y stock
        self.meses_garantia = garantia  # garantía en meses(atributo propio)

    def __str__(self):
    #sobrescribimos __str__ para incluir la información de la garantía
        return f"ProductoElectronico(id={self.id}, nombre={self.nombre}, precio={self.precio}, stock={self.stock}, meses_garantia={self.meses_garantia})"

#subclase ProductoRopa que hereda de Producto y añade el atributo talla y color
class ProductoRopa(Producto):
    def __init__(self, nombre: str, precio: float, stock: int, talla: str, color: str):
        super().__init__(nombre, precio, stock) #llamamos al constructor de la clase padre para inicializar id, nombre, precio y stock
        self.talla = talla  #talla de la prenda (atributo propio)
        self.color = color  #color de la prenda (atributo propio)

    def __str__(self):
    #sobrescribimos __str__ para incluir la información de la talla y color
        return f"ProductoRopa(id={self.id}, nombre={self.nombre}, precio={self.precio}, stock={self.stock}, talla={self.talla}, color={self.color})"
