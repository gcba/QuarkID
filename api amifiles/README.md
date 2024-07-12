# API de Gestión de Archivos en Azure Blob Storage

Este proyecto proporciona una API para subir y descargar archivos en Azure Blob Storage con soporte para tokens de un solo uso y eliminación automática de archivos.

## Requisitos

- Docker
- Docker Compose

## Configuración

Incluir  las siguientes variables de entorno están definidas correctamente en tu `docker-compose.yml`:

- `ACCOUNT_NAME`: El nombre de tu cuenta de almacenamiento de Azure.
- `ACCOUNT_KEY`: La clave de acceso de tu cuenta de almacenamiento de Azure.
- `BLOB_SERVICE_URL`: La URL del servicio de blobs de tu cuenta de almacenamiento de Azure.
- `API_SERVICE_URL`: La URL del servicio de la API.

## Uso

## Endpoints
### Subir un archivo

URL: /upload
Método: POST
Descripción: Sube un archivo a Azure Blob Storage y devuelve una URL de descarga con un token de un solo uso.

Ejemplo de solicitud:

```sh
curl -X POST "{API_SERVICE_URL}/upload" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@ruta/al/archivo"
```

Respuesta:

```sh
{
  "message": "Archivo archivo.pdf subido exitosamente con nombre único <unique_id>.pdf.",
  "download_url": "{API_SERVICE_URL}/download/ami/<unique_id>.pdf?token=<token_id>"
}
```
###Descargar un archivo

URL: /download/{container_name}/{blob_name}?token={token}
Método: GET
Descripción: Descarga un archivo de Azure Blob Storage usando un token de un solo uso. El archivo se elimina después de la descarga.

Ejemplo de solicitud:

```sh
curl -o "{API_SERVICE_URL}/download/ami/<unique_id>.pdf?token=<token_id>"
```
