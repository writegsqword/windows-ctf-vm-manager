import asyncio
import select
import subprocess
import pipeproxy

MONITOR_SOCK_PATH = "monitor.sock"
FORWARD_SOCK_PATH = "forward.sock"
class VMInstance:
    async def _vm_init(self):
        self.vm_subproc = asyncio.create_subprocess_exec("bash", 
        "./scripts/entrypoint.sh", \
        self.workingdir, 
        self.imgdir, 
        self.monitor_sock, 
        self.forward_sock,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )
        await self._vm_reset()
        
    async def _vm_reset(self):
        proc = await asyncio.create_subprocess_exec("bash",
        "./scripts/load_snapshot.sh",
        self.monitor_sock,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )
        _ = await proc.communicate()
        self.ready = True



    def is_ready(self):
        return self.ready

    def __init__(self, imgdir : str, workingdir : str):
        self.ready : bool = False
        self.imgdir : str = imgdir
        self.workingdir : str = workingdir
        self.monitor_sock : str = f"{workingdir}/{MONITOR_SOCK_PATH}"
        self.forward_sock : str = f"{workingdir}/{FORWARD_SOCK_PATH}"
        self.vm_subproc = False

    async def serve(self, in_writer, in_reader):
        #dont serve if not ready
        if not self.is_ready():
            return
        #TODO: fix race condition(if it becomes a problem)
        self.ready = False
        remote_reader, remote_writer = await asyncio.open_unix_connection(self.forward_sock)
        await pipeproxy.handle_client(in_reader, in_writer, remote_reader, remote_writer)
        await self._vm_reset()



