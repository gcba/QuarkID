from fastapi import APIRouter, HTTPException
from kink import inject
from services.serv_web3 import Web3Service
from pydantic import BaseModel


class URLDto(BaseModel):
    url: str


class VCSLDto(BaseModel):
    id: str
    ipns: str


@inject
class Web3Router:
    def __init__(self, web3_service: Web3Service):
        self.web3_service: Web3Service = web3_service
        self.router = APIRouter()
        # Add routes
        self.router.add_api_route("/web3/issuer-url", self.set_issuer_url, methods=["POST"])
        self.router.add_api_route("/web3/issuer-url", self.get_issuer_url, methods=["GET"])
        self.router.add_api_route("/web3/vcsl", self.add_vcsl, methods=["POST"])
        self.router.add_api_route("/web3/vcsl/{id}", self.get_vcsl, methods=["GET"])

    async def set_issuer_url(self, url: URLDto):
        if url is None or url.url is None:
            raise HTTPException(status_code=400, detail="URL not provided")
        ok = self.web3_service.set_issuer_url(url.url)
        if not ok:
            raise HTTPException(status_code=500, detail="Error setting issuer URL")
        return {"status": "OK"}

    async def add_vcsl(self, data: VCSLDto):
        if data is None or data.id is None or data.ipns is None:
            raise HTTPException(status_code=400, detail="Data not provided")
        ok = self.web3_service.add_vcsl(data.id, data.ipns)
        if not ok:
            raise HTTPException(status_code=500, detail="Error adding vcsl")
        return {"status": "OK"}

    async def get_issuer_url(self):
        return {"url": self.web3_service.get_issuer_url()}

    async def get_vcsl(self, id: str):
        return {"ipns": self.web3_service.get_vcsl(id)}
