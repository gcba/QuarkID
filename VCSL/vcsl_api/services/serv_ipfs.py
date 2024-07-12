import requests
from kink import inject
from models.bitarray import BitArray
from models.ipfs_dto import IPFSDto
from misc.scheduler import Scheduler
from services.serv_key import KeyService


@inject
class IPFSService:
    def __init__(self,
                 ipfs_api_url: str,
                 key_service: KeyService,

                 scheduler: Scheduler
                 ):
        self.ipfs_api_url = ipfs_api_url
        self.key_service = key_service
        self.scheduler = scheduler

    def create_key(self, key_name: str) -> bool:
        key = self.key_service.generate()
        key = key.replace('\n', '$')
        print(key)
        key_name = key_name.replace('\n', '')
        data = {
            'key': key,
            'name': key_name
        }
        response = requests.post(f'{self.ipfs_api_url}/key', json=data)
        if response.status_code != 200:
            print(response.text)
            return False
        return True

    def add_vcsl(self, bit_array: BitArray, bit_array_id: str, key_name: str) -> IPFSDto:
        key_name = key_name.replace('\n', '')
        data = {
            'bitarray': bit_array.compress().decode('ascii'),
            'key_name': key_name
        }
        response = requests.post(f'{self.ipfs_api_url}/bitarray/{bit_array_id}', json=data)
        if response.status_code != 200:
            print(response.text)
            raise Exception("IPFS upload failed")
        return IPFSDto(cid=response.json()['cid'], ipns=response.json()['ipns'])

    def update_vcsl(self, bitarray: BitArray):
        key_name = bitarray.id.replace('\n', '')
        data = {
            'bitarray': bitarray.compress().decode('ascii'),
            'key_name': key_name
        }
        response = requests.post(f'{self.ipfs_api_url}/bitarray/{bitarray.id}', json=data)
        print(f"[IPFS Service] Response: {response.json()}")
        if response.status_code != 200:
            print(f"[IPFS Service] Error updating bitarray {bitarray.id}")
            print(f"[IPFS Service] {response.text}")
            # raise Exception("IPFS upload failed")
        print("[IPFS Service] Updated bitarray in IPFS")
        return IPFSDto(cid=response.json()['cid'], ipns=response.json()['ipns'])
