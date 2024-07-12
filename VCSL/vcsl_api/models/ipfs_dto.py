class IPFSDto:
    def __init__(self, cid: str, ipns: str):
        self.cid = cid
        self.ipns = ipns

    def to_dict(self):
        return {
            'cid': self.cid,
            'ipns': self.ipns
        }

    def get_cid(self):
        return self.cid

    def get_ipns(self):
        return self.ipns

    def __str__(self):
        return f"IPFSDto(cid={self.cid}, ipns={self.ipns})"
