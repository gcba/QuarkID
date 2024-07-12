from fastapi import FastAPI, File, UploadFile, HTTPException
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions, BlobClient
from fastapi.responses import StreamingResponse
from datetime import datetime, timedelta
import io
import uuid
import os

app = FastAPI()


account_name = os.getenv('ACCOUNT_NAME')
account_key = os.getenv('ACCOUNT_KEY')
blob_service_url = os.getenv('BLOB_SERVICE_URL')
api_service_url = os.getenv('API_SERVICE_URL')

blob_service_client = BlobServiceClient(account_url=blob_service_url, credential=account_key)

single_use_tokens = {}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        container_name = "amifiles"
                
        unique_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        blob_name = f"{unique_id}{file_extension}"

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(file.file, overwrite=True)

        # Generar un token SAS para el archivo subido
        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=container_name,
            blob_name=blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True, delete=True),
            expiry=datetime.utcnow() + timedelta(minutes=1440)
        )

        
        token_id = str(uuid.uuid4())
        download_url = f"{api_service_url}/download/{container_name}/{blob_name}?token={token_id}"


        single_use_tokens[token_id] = {
            "sas_token": sas_token,
            "blob_name": blob_name,
            "container_name": container_name,
            "used": False
        }

        return {"message": f"Archivo {file.filename} subido exitosamente con nombre único {blob_name}.", "download_url": download_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{container_name}/{blob_name}")
async def download_file(container_name: str, blob_name: str, token: str):
    try:
        
        if token not in single_use_tokens:
            raise HTTPException(status_code=404, detail="Token no válido o ya usado.")
        
        token_info = single_use_tokens[token]
        if token_info["used"]:
            raise HTTPException(status_code=404, detail="Token no válido o ya usado.")
        
        
        single_use_tokens[token]["used"] = True
        
        sas_token = token_info["sas_token"]
        blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
        blob_client = BlobClient.from_blob_url(blob_url)

        stream = blob_client.download_blob()
        data = stream.readall()

        # Eliminar el archivo del blob storage
        blob_client.delete_blob()

        return StreamingResponse(io.BytesIO(data), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={blob_name}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
