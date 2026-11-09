# Tienda online

**Autora:** Helena Pérez

## Descripción

API REST de una tienda online hecha con Python y FastAPI (Práctica 2). Permite:

- Gestionar **usuarios** (clientes y administradores).
- Gestionar **productos** (genéricos, electrónicos y ropa).
- Crear **pedidos** (solo los clientes) y consultar su historial.

Los datos se guardan en memoria, así que se pierden al parar la aplicación.

## Estructura

```
.
├── src/                  # código de la aplicación
│   ├── main.py           # punto de entrada (endpoints de la API)
│   ├── schemas.py        # esquemas de entrada y salida (Pydantic)
│   ├── models/           # clases Usuario, Producto y Pedido
│   └── services/         # TiendaService (lógica de la tienda)
├── dockerfile            # receta de la imagen de Docker
├── .dockerignore         # ficheros que no entran en la imagen
├── requirements.txt      # dependencias con versiones fijadas
└── README.md
```

## Ejecutar sin Docker

```bash
pip install -r requirements.txt
cd src
python main.py
```

La API queda en http://localhost:8000 y la documentación interactiva en http://localhost:8000/docs.

## Docker

### 1. Construir la imagen

```bash
docker build -t tienda-online:1.0 .
```

### 2. Ejecutar el contenedor

```bash
# Puerto por defecto (8000)
docker run --rm -p 8000:8000 tienda-online:1.0

# En segundo plano y con nombre
docker run -d --name tienda -p 8000:8000 tienda-online:1.0

# Cambiando el puerto con la variable de entorno PORT
docker run --rm -e PORT=9000 -p 9000:9000 tienda-online:1.0
```

Para parar y borrar el contenedor en segundo plano: `docker stop tienda && docker rm tienda`.

### 3. Variables de entorno

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `PORT`   | `8000`            | Puerto en el que escucha la API dentro del contenedor |

La aplicación no usa claves ni secretos.

### 4. Salida esperada y pasos de prueba

Al arrancar el contenedor se debe ver algo parecido a:

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Pasos de prueba (con el contenedor en marcha):

1. Abre http://localhost:8000/docs: debe aparecer la documentación de la API.
2. Crea un cliente:
   ```bash
   curl -X POST http://localhost:8000/usuarios -H "Content-Type: application/json" \
     -d '{"nombre":"Ana","email":"ana@mail.com","tipo":"cliente","direccion":"Calle Sol 1"}'
   ```
   Respuesta esperada (código 201): `{"id":"<uuid>","nombre":"Ana","email":"ana@mail.com","es_admin":false}`
3. Crea un producto:
   ```bash
   curl -X POST http://localhost:8000/productos -H "Content-Type: application/json" \
     -d '{"tipo":"electronico","nombre":"Portatil","precio":799.99,"stock":5,"meses_garantia":24}'
   ```
   Respuesta esperada (código 201): `{"id":"<uuid>","tipo":"electronico","nombre":"Portatil","precio":799.99,"stock":5,"meses_garantia":24}`
4. Crea un pedido con los dos `id` anteriores:
   ```bash
   curl -X POST http://localhost:8000/pedidos -H "Content-Type: application/json" \
     -d '{"cliente_id":"<id del cliente>","items":[{"producto_id":"<id del producto>","cantidad":2}]}'
   ```
   Respuesta esperada (código 201): un pedido con `"total":1599.98`.
5. Comprueba que el stock bajó: `curl http://localhost:8000/productos` debe mostrar `"stock":3`.
6. Pide más unidades de las que hay (por ejemplo `"cantidad":99`): debe responder con error 400 y el mensaje `Stock insuficiente de 'Portatil' (disponible: 3, solicitado: 99).`

### 5. Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/usuarios` | Crear usuario |
| GET | `/usuarios` | Listar usuarios |
| GET | `/usuarios/{usuario_id}` | Ver un usuario |
| GET | `/usuarios/{cliente_id}/pedidos` | Historial de pedidos de un cliente |
| POST | `/productos` | Crear producto |
| GET | `/productos` | Listar productos |
| GET | `/productos/{producto_id}` | Ver un producto |
| DELETE | `/productos/{producto_id}` | Eliminar un producto |
| POST | `/pedidos` | Crear pedido |

### 6. Publicar y descargar la imagen (registry)
La imagen está publicada en https://hub.docker.com/r/helenaperezz/tienda-online. 

```bash
docker login
docker tag tienda-online:1.0 helenaperezz/tienda-online:1.0
docker push helenaperezz/tienda-online:1.0
```

Para descargarla y ejecutarla desde cualquier equipo:

```bash
docker pull helenaperezz/tienda-online:1.0
docker run --rm -p 8000:8000 helenaperezz/tienda-online:1.0
```

## Flujo de trabajo con Git

- `main`: rama principal, siempre con código funcional.
- `feature/docker`: contenerización de la aplicación. Se integra en `main` mediante Pull Request.
