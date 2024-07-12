from azure.storage.blob import generate_container_sas, BlobSasPermissions
from datetime import datetime, timedelta

# Datos de la cuenta 
account_name = os.getenv('ACCOUNT_NAME')
account_key = os.getenv('ACCOUNT_KEY')

# Crear token SAS
sas_token = generate_container_sas(
    account_name=account_name,
    container_name="ami",
    account_key=account_key,
    permission=BlobSasPermissions(read=True, write=True, delete=True, list=True),  # Agrega los permisos necesarios
    expiry=datetime.utcnow() + timedelta(days=1)  # Ajusta la expiración según sea necesario
)

print(f"?{sas_token}")  # Imprime el token SAS con un signo de interrogación al inicio
