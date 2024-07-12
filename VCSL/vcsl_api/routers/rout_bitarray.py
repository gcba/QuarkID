from fastapi import APIRouter, HTTPException, BackgroundTasks
from kink import inject
from services.serv_bitarray import BitArrayService


@inject
class BitArrayRouter:
    def __init__(self, bit_array_service: BitArrayService):
        self.bit_array_service: BitArrayService = bit_array_service
        self.router = APIRouter()
        self.router.add_api_route(path="/bit-array", endpoint=self.create_bit_array, methods=["PUT"],)
        self.router.add_api_route(path="/bit-array/{uuid}", endpoint=self.get_compressed_bit_array, methods=["GET"])
        self.router.add_api_route(path="/bit-array/{uuid}/free", endpoint=self.get_free_bits, methods=["GET"])
        self.router.add_api_route(path="/bit-array/{uuid}/index", endpoint=self.acquire_index, methods=["PUT"])
        self.router.add_api_route(path="/bit-array/{uuid}/{index}", endpoint=self.flip_bit, methods=["POST"])
        self.router.add_api_route(path="/bit-array/{uuid}/{index}", endpoint=self.get_bit_array_element, methods=["GET"])

    async def create_bit_array(self, background_tasks: BackgroundTasks):
        bit_array_uuid, bit_array = await self.bit_array_service.create_bit_array()
        background_tasks.add_task(self.bit_array_service.upload_bit_array, bit_array_uuid, bit_array)
        return {"id": bit_array_uuid}

    async def acquire_index(self, uuid: str):
        new_index = await self.bit_array_service.acquire_bit_array_index(uuid)
        if new_index == -1:
            raise HTTPException(status_code=404, detail="No free bits")
        return {"index": new_index}

    async def flip_bit(self, uuid: str, index: int):
        ok = await self.bit_array_service.flip_bit(uuid, index)
        if (not ok):
            raise HTTPException(status_code=500, detail="Bit flip failed")
        return {"message": "Bit flipped"}

    async def get_compressed_bit_array(self, uuid: str):
        bit_array, _ = await self.bit_array_service.get_bit_array(uuid)
        if (bit_array is None):
            raise HTTPException(status_code=404, detail="Bit array not found")
        return {"bit-array": bit_array.compress()}

    async def get_bit_array_element(self, uuid: str, index: int):
        bit_array, _ = await self.bit_array_service.get_bit_array(uuid)
        if bit_array is None:
            raise HTTPException(status_code=404, detail="Bit array not found")
        if index >= bit_array.size:
            raise HTTPException(status_code=404, detail="Index out of bounds")
        bit = bit_array[index]
        return {"bit": bit}

    async def get_free_bits(self, uuid: str):
        free_bits = await self.bit_array_service.get_free_bits(uuid)
        if free_bits == -1:
            raise HTTPException(status_code=404, detail="Bit array not found")
        return {"free": free_bits}
