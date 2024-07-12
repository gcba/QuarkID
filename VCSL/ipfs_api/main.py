import dto
from sys import stderr
from fastapi import FastAPI, HTTPException
from subprocess import Popen, PIPE
from asyncio import sleep
from random import randint

app = FastAPI()


@app.on_event("startup")
async def init_ipfs():
    print("Initializing IPFS", file=stderr)
    Popen("./start_ipfs.sh", stdout=PIPE, stderr=PIPE, shell=True)
    await sleep(5)


@app.get("/")
async def health_check():
    # Return 200 OK
    return {}


@app.post("/key")
async def create_key(key: dto.KeyDTO):
    # Create key
    rnd_file_name = f"{randint(0, 1000000000000)}.pem"
    f_key = key.key.replace("$", "\n")
    cmds = [
        f"echo '{f_key}' > {rnd_file_name}",
        f"ipfs key import {key.name} {rnd_file_name} --format=pem-pkcs8-cleartext",
        f"rm {rnd_file_name}"
    ]

    def remove_pem():
        Popen(f"rm {rnd_file_name}", stdout=PIPE, stderr=PIPE, shell=True)

    # Populate the file
    subp = Popen(cmds[0], stdout=PIPE, stderr=PIPE, shell=True)
    out, err = subp.communicate()
    if subp.returncode != 0:
        print(err.decode("utf-8"), file=stderr)
        remove_pem()
        raise HTTPException(status_code=500, detail="Error importing key (1)")

    # Import the key
    subp = Popen(cmds[1], stdout=PIPE, stderr=PIPE, shell=True)
    out, err = subp.communicate()
    if subp.returncode != 0:
        if err.decode("utf-8").find("already exists") != -1:
            print(f"Key {key.name} already exists", file=stderr)
        else:
            print(f'Error: {err.decode("utf-8")}', file=stderr)
            remove_pem()
            raise HTTPException(status_code=500, detail="Error importing key (2)")

    # Remove the file
    remove_pem()
    return "OK"


@app.post("/bitarray/{id}")
async def upload_bitarray(id: str, bitarray: dto.BitArrayDTO):
    # Check if the key exists
    subp = Popen(f"ipfs key list -l | grep {bitarray.key_name}", stdout=PIPE, stderr=PIPE, shell=True)
    out, err = subp.communicate()
    if subp.returncode != 0 or len(out) == 0:
        print(f'Error: {err.decode("utf-8")}', file=stderr)
        print(f'Out: {out.decode("utf-8")}', file=stderr)
        return {"error": "Key not found"}

    # Add the bitarray
    subp = Popen(f"echo {bitarray.bitarray} | ipfs add -Q --cid-version=1", stdout=PIPE, stderr=PIPE, shell=True)
    out, err = subp.communicate()
    if subp.returncode != 0:
        print(err.decode("utf-8"), file=stderr)
        return {"error": "Error adding bitarray to IPFS"}

    cid = out.decode("utf-8").strip()
    print(f"New cid for {id}: {cid}")

    # Publish under the name
    subp = Popen(f"ipfs name publish -Q --key={bitarray.key_name} {cid}", stdout=PIPE, stderr=PIPE, shell=True)
    out, err = subp.communicate()
    if subp.returncode != 0:
        print(err.decode("utf-8"), file=stderr)
        return {"error": "Error publishing bitarray to IPNS"}

    ipns = out.decode("utf-8").strip()
    return {"cid": cid, "ipns": ipns}


@app.get("/bitarray/{id}")
async def get_bitarray(id: str):
    # Do an ipfs cat on the IPNS
    subp = Popen(f"ipfs cat /ipns/{id}", stdout=PIPE, stderr=PIPE, shell=True)
    out, err = subp.communicate()
    if subp.returncode != 0:
        print(err.decode("utf-8"), file=stderr)
        return {"error": "Error getting bitarray from IPNS"}
    return {"bitarray": out.decode("ascii").strip()}
