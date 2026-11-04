# ARCHIVO CON CLASE PADRE USUARIO Y SUBCLASES CLIENTE Y ADMINISTRADOR
# clase padre Usuario (tiene todo lo común a cualquier usuario de la tienda: id, nombre, email)

#importar biblioteca uuid para generar identificadores únicos automáticamente
import uuid

# Clase padre Usuario
class Usuario:
    def __init__(self, nombre: str, email: str):
        self.id = str(uuid.uuid4())  # Genera un identificador único aleatorio. Se convierte a str para facilitar su uso.
        self.nombre = nombre
        self.email = email
        
    def is_admin(self) -> bool:
        # Por defecto, un usuario NO es administrador, asique por defecto devuelve False.
        return False

    def __str__(self):
        # Representación del usuario que luego se sobreescribirá en las subclases.
        return f"Usuario(id={self.id}, nombre={self.nombre}, email={self.email})"
    
#subclase Cliente que hereda de Usuario y añade el atributo direccion postal
class Cliente(Usuario):
    def __init__(self, nombre: str, email: str, direccion: str):
        super().__init__(nombre, email) #llamamos al constructor de la clase padre para inicializar id, nombre y email
        self.direccion = direccion  #direccion postal del cliente (atributo propio)

    def __str__(self):
        #sobreescribimos __str__ para incluir la información de la dirección postal
        return f"Cliente(id={self.id}, nombre={self.nombre}, email={self.email}, direccion={self.direccion})"
    
#subclase Administrador que hereda de Usuario y sobrescribe el método is_admin para indicar que es administrador
class Administrador(Usuario):
    def is_admin(self) -> bool:
        # Un administrador SI es administrador, asique sobreescribimos el método para devolver True.
        return True

    def __str__(self):
        #sobreescribimos __str__ para indicar que es administrador
        return f"Administrador(id={self.id}, nombre={self.nombre}, email={self.email})"