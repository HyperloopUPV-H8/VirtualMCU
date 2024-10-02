from multiprocessing import shared_memory


class CTRLMap:
    _mem_size = 1024 # TODO: adjust this value

    def __init__(self, name: str, create: bool = True):
        self._mem = shared_memory.SharedMemory(
            name=f"vmcu__ctrl__{name}",
            create=create,
            size=self._mem_size
        )

    def close(self):
        self._mem.close()
        self._mem.unlink()
