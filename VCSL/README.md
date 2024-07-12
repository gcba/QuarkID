#
# Verifiable Credential Status List
---
## Summary
The VCSL (Verifier Credential Status List) system addresses the need in the verifiable credentials domain for a mechanism to verify the validity or revocation status of credentials. Utilizing a bit array structure, where each bit signifies the status of a verifiable credential (0 for valid, 1 for revoked), the system employs persistence methods like IPFS, blockchain, and an SQL database. It enables issuers to create, manipulate, and query bit arrays, offering flexibility for direct issuer system queries or decentralized solutions through IPFS, providing a comprehensive approach to credential verification.

# Components:
### VCSL API
This is the main component, is the one that has all the endpoints for the issuer to admin the system, and for any issuer to query about some VCSL.

### IPFS API
This is an API fot the IPFS component of the system. It controls the uploading and naming on IPNS.

### PostgreSQL
This is the SQL solution for a database in the system

### Redis
This Redis service is used for locks

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
