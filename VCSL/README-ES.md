#
# Lista de Estado de Credenciales Verificables
---
## Resumen
El sistema VCSL (Lista de Estado de Credenciales Verificables) aborda la necesidad en el ámbito de credenciales verificables de un mecanismo para verificar la validez o estado de revocación de las credenciales. Utilizando una estructura de matriz de bits, donde cada bit significa el estado de una credencial verificable (0 para válido, 1 para revocado), el sistema emplea métodos de persistencia como IPFS, blockchain y una base de datos SQL. Permite a los emisores crear, manipular y consultar matrices de bits, ofreciendo flexibilidad para consultas directas al sistema del emisor o soluciones descentralizadas a través de IPFS, proporcionando un enfoque integral para la verificación de credenciales.

## Componentes:

### API de VCSL

La API de VCSL es el componente principal, abarcando todos los puntos finales para la administración del sistema por parte del emisor. También proporciona puntos finales para que cualquier emisor consulte información sobre VCSL específicos.

### API de IPFS

La API de IPFS gestiona las interacciones con el componente IPFS del sistema. Es responsable de manejar la carga de archivos y gestionar el nombramiento en IPNS.

### PostgreSQL

PostgreSQL sirve como la solución de base de datos SQL para el sistema, brindando capacidades robustas de almacenamiento y recuperación de datos.

### Redis

El servicio Redis desempeña un papel crucial en el sistema, utilizado principalmente para implementar bloqueos que aseguran la consistencia de los datos y evitan conflictos.

# Componentes:
### API de VCSL
Este es el componente principal, es el que tiene todos los puntos finales para que el emisor administre el sistema y para que cualquier emisor consulte sobre algún VCSL.

### API de IPFS
Esta es una API para el componente IPFS del sistema. Controla la carga y el nombramiento en IPNS.

### PostgreSQL
Esta es la solución SQL para una base de datos en el sistema.

### Redis
Este servicio Redis se utiliza para bloqueos.

## Endpoints
### Health Check

- **Path:** `/health-check`
- **HTTP Method:** `GET`
- **Summary:** Health Check
- **Request:**
  - No request parameters

---

### Create Bit Array

- **Path:** `/bit-array`
- **HTTP Method:** `PUT`
- **Summary:** Create Bit Array
- **Request:**
  - No request parameters

---

### Get Compressed Bit Array

- **Path:** `/bit-array/{uuid}`
- **HTTP Method:** `GET`
- **Summary:** Get Compressed Bit Array
- **Request:**
  - Path Parameters:
    - `uuid` (string, required)

---

### Get Free Bits

- **Path:** `/bit-array/{uuid}/free`
- **HTTP Method:** `GET`
- **Summary:** Get Free Bits
- **Request:**
  - Path Parameters:
    - `uuid` (string, required)

---

### Acquire Index

- **Path:** `/bit-array/{uuid}/index`
- **HTTP Method:** `PUT`
- **Summary:** Acquire Index
- **Request:**
  - Path Parameters:
    - `uuid` (string, required)

---

### Flip Bit

- **Path:** `/bit-array/{uuid}/{index}`
- **HTTP Method:** `POST`
- **Summary:** Flip Bit
- **Request:**
  - Path Parameters:
    - `uuid` (string, required)
    - `index` (integer, required)

---

### Get Issuer Url

- **Path:** `/web3/issuer-url`
- **HTTP Method:** `GET`
- **Summary:** Get Issuer Url
- **Request:**
  - No request parameters

---

### Set Issuer Url

- **Path:** `/web3/issuer-url`
- **HTTP Method:** `POST`
- **Summary:** Set Issuer Url
- **Request:**
  - Request Body:
    - Content Type: `application/json`
      - Schema: 
      ```json
      {
        'url': string
      }
      ```

---

### Add Vcsl

- **Path:** `/web3/vcsl`
- **HTTP Method:** `POST`
- **Summary:** Add Vcsl
- **Request:**
  - Request Body:
    - Content Type: `application/json`
      - Schema: 
      ```json
      {
        'id': string,
        'ipns': string
      }
      ```

---

### Get Vcsl

- **Path:** `/web3/vcsl/{id}`
- **HTTP Method:** `GET`
- **Summary:** Get Vcsl
- **Request:**
  - Path Parameters:
    - `id` (string, required)
 VCSL
