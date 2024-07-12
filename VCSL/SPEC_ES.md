# Introducción
Se necesita de un sistema que funcione como fuente confiable para reconocer el estado (válido o inválido) de una credencial. Se necesita que este sistema sea decentralizado, que pueda ser consultado a través de distintos sistemas y que no dependa de un sólo proveedor para acceder a la información. 

# Actores
### Issuer
Entidad quién emite la credencial. Es el responsable de agregar a la misma toda la información necesaria para que el holder de la misma, o un verifier, pueda consultar su estado de manera independiente.
### Holder
Entidad quién tiene la credencial.
### Verifier
Entidad quién necesita consultar la validez de la credencial.
# Solución
Se opta por la utilización de un bit array, esto es, un listado de bits. Cada bit corresponde a una credencial verficable. Si su valor el 1, entonces la credencial esta revocada, sino, significa que la credencial es válida. Cada credencial tendrá un puntero al bit array en donde se encuentra registrada junto con un índice para saber en dónde se encuentra. 
El puntero al bit array debe apuntar a algún endpoint decentralizado para que cualquier persona pueda requerirlo en cualquier momento, y no dependa del issuer.
El issuer debe tener el bit array totalmente inicializado en 0, al dar de alta una credencial, este debe elegir un índice desocupado y lockearlo. 
Un holder o verifier debe poder acceder al bit string a la hora de verificar una credencial. Consultando el elemento ubicado en el índice mostrado por la credencial.

# Requisitos funcionales
- Un issuer debe poder crear una bit array para guardar el estado de sus credenciales de manera decentralizada.
- Un issuer debe poder asignar un índice aleatorio a una credencial a la hora de emitir una nueva VC.
- Un issuer debe poder revocar una VC en el bit array haciendo que su bit corresponda a un 1.
- Un holder/verifier debe poder consultar el bit array creado por un issuer solamente con la información en la credencial.

# Requisitos no funcionales
- La consulta de un bit array debe poder hacerse en cualquier momento.
- Debe haber una instancia pública y decentralizada del bit array en todo momento.

# Diagrama
![[VCSL.svg]]

# Componentes
### API REST
Api por la cual el issuer interactúa con el sistema. Permite crear las bit arrays y actualizarlas. Es quién se encarga de comunicarse con el smart Contract e IPFS. 

### Back Up Batch
Componente opcional para hacer un backup de lo persistido en IPFS y el Smart Contract. Este debe poder guardar dicho backup en alguna solución de storage (AWS S3, Google Cloud Storage, On premise database).

### Bit Array List Smart Contract
Smart contract deployado en la red de zkSync. Funciona como mapa de nombres para bitarrays. La estructura que guarda es:
```js
id -> 
   (IPNS de bit array, 
	IPNS de historial, 
	timestamp de creación)
```


### IPFS
Componente de persistencia. Para poder actualizar el bit array se necesita utilizar IPNS, de lo contrario, el CID del bit array cambiará cada vez que se necesite actaulizará el mismo. Además, se guardará en otro IPNS un archivo con los historiales de cambio (1 por linea) del archivo del bit array.
El archivo de historial se verá:
```
QmScmAUxyqnW1JNH17oQDCbjDZsZHYiuti55d6FxjLrwk1 1704663383
QmTbjFUZ4P82gapCfoQXKR6DeiXNXxPfvkzsS6smp2M1wX 1704664437
QmTyrwT8QMX7fBfkxjrzxWwTSiyBHJjp7ydb4XVpfZMZWq 1704680937
...
```
En donde el CID apunta al archivo del bit array en una versión anterior y el timestamp a cuando fue actualizado.

# Observaciones de diseño
### Datos en la VC
Una verifiable credential debe agregar datos para poder saber a dónde ir a buscar su estado:
```json
{
	"@context": [
	    "https://www.w3.org/ns/credentials/v2",
	    "https://www.w3.org/ns/credentials/examples/v2"
	  ],
	...
	...
	
	"credentialStatus": {
	    "type": "bitArrayStatusEntry",
	    "persistanceType": "IPFS",
	    "bitArrayAddress": "k51qzi5uqu5dhyk7e8gbtkjpix6e3wfyknh8n2zd0cpmrcnu8xsqmkx82usgin",
	    "bitArrayIndex": 5432,
	    "bitArraySC": "0xde2b7414e2918a393b59fc130bceb75c3ee52493",
		"bitArrayID": 5
		}
},
```

### Tamaño de la bit array
En un principio no existen limitaciones en el tamaño del bit array, ya que este es subido a IPFS. Se proponen 16 KiB entradas, para asemejarse a la propuesta de DIF.

# Mejoras en futuras versiones
### Manejo de historial
El historial de cambios puede ser tranquilamente manipulado por el dueño de la key de IPNS, pudiéndolo modificar en caso de querer ser malicioso. Debe pensarse una manera de solucionar esto haciendo que el historial sea decentralizado y barato.

### Credenciales de múltiples estados
Por el momento sólo se pueden guardar dos estados "válido y revocado". En un futuro puede adaptarse el sistema para que una credencial tenga 2^n estados, haciendo que cada elemento del bit array ocupe n bits.
