import random
import sys
from kink import inject
from services.abstractClasses.serv_cache_i import ICacheService
from services.abstractClasses.serv_lock_i import ILockService
from services.serv_web3 import Web3Service
from services.serv_ipfs import IPFSService
from persistance.dao_bitarray import BitArrayDAO
from models.bitarray import BitArray
from models.ipfs_dto import IPFSDto
from misc.scheduler import Scheduler
from uuid import uuid4
from datetime import datetime


@inject
class BitArrayService:
    def __init__(self,
                 cache_service: ICacheService,
                 lock_service: ILockService,
                 bitarray_dao: BitArrayDAO,
                 web3_service: Web3Service,
                 ipfs_service: IPFSService,
                 scheduler: Scheduler
                 ):

        self.bitarray_dao: BitArrayDAO = bitarray_dao
        self.cache_service: ICacheService = cache_service
        self.lock_service: ILockService = lock_service
        self.ipfs_service: IPFSService = ipfs_service
        self.web3_service: Web3Service = web3_service
        self.scheduler: Scheduler = scheduler

        print(f"All bitarrays: {self.bitarray_dao.get_all_bitarrays()}")
        print(f"Total: {len(self.bitarray_dao.get_all_bitarrays())}")

        self.scheduler.add_job(self.update_bitarrays_in_ipfs, 'interval', hours=5, next_run_time=datetime.now())

    async def create_bit_array(self) -> (str, BitArray):
        bit_array_uuid = str(uuid4())
        bit_array = BitArray(id=bit_array_uuid)
        await self.lock_service.acquire_lock(bit_array_uuid)
        self.bitarray_dao.set_bitarray(bit_array)
        self.bitarray_dao.set_mask(bit_array)
        await self.lock_service.release_lock(bit_array_uuid)
        return bit_array_uuid, bit_array

    def upload_bit_array(self, id: str, bitarray: BitArray) -> None:
        keyCreated = self.ipfs_service.create_key(key_name=id)
        if not keyCreated:
            raise Exception("IPFS Key creation failed")
        try:
            ipfs_dto: IPFSDto = self.ipfs_service.add_vcsl(bit_array=bitarray, bit_array_id=id, key_name=id)
        except Exception as e:
            print(e, file=sys.stderr)
            return

        # Now, upload it to the smart contract
        result = self.web3_service.add_vcsl(id=id, ipns=ipfs_dto.get_ipns())
        if not result:
            raise Exception("VCSL upload failed")

    async def get_bit_array(self, bit_array_uuid: str, cached=True) -> (BitArray, BitArray):
        compressed_bit_array = self.bitarray_dao.get_bitarray(bit_array_uuid)
        compressed_mask = self.bitarray_dao.get_mask(bit_array_uuid)
        return compressed_bit_array, compressed_mask

    async def acquire_bit_array_index(self, bit_array_uuid: str) -> int:
        lock = await self.lock_service.acquire_lock(bit_array_uuid, blocking=True)
        if lock is None:
            return -1
        bit_array: BitArray = None
        mask: BitArray = None
        try:
            bit_array, mask = await self.get_bit_array(bit_array_uuid)
        except Exception:
            return -1

        if bit_array.free == 0:
            await self.lock_service.release_lock(bit_array_uuid)
            return -1

        index = random.randint(0, bit_array.size - 1)
        while bit_array[index] == 1:
            index = random.randint(0, bit_array.size - 1)

        mask[index] = 1
        self.bitarray_dao.set_mask(mask)
        await self.lock_service.release_lock(bit_array_uuid)
        return index

    async def flip_bit(self, bit_array_uuid: str, index: int) -> bool:
        lock = await self.lock_service.acquire_lock(bit_array_uuid, blocking=True)
        if lock is None:
            return False
        bit_array: BitArray = None
        mask: BitArray = None
        try:
            bit_array, mask = await self.get_bit_array(bit_array_uuid)
        except Exception:
            return False
        if mask[index] == 0:
            return False
        bit_array[index] = not bit_array[index]

        self.bitarray_dao.set_bitarray(bit_array)
        await self.lock_service.release_lock(bit_array_uuid)
        return True  # TODO: Check if there was an error and return false

    async def get_free_bits(self, bit_array_uuid: str) -> int:
        try:
            bit_array, mask = await self.get_bit_array(bit_array_uuid)
        except Exception:
            return -1
        return mask.free

    def update_bitarrays_in_ipfs(self):
        bitarrays = self.bitarray_dao.get_all_bitarrays()
        for bitarray in bitarrays:
            try:
                dto: IPFSDto = self.ipfs_service.update_vcsl(bitarray)
                print(f"Result: {dto}")
            except Exception as e:
                print(f"Error updating bitarray {bitarray.id} in IPFS")
                print(e, file=sys.stderr)
                break
