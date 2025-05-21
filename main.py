import asyncio
import vminstance
from vminstance import VMInstance
import os




G_vms: list[VMInstance] = []
VM_IMG = os.path.abspath("./vm/img")
VM_WORKDIR = os.path.abspath("./vm/working")


async def initialize():
    global G_vms
    #todo: figure out how to call init in consturctor
    vm0 = vminstance.VMInstance(VM_IMG, VM_WORKDIR)
    await vm0._vm_init()
    G_vms.append(vm0)




async def server_proc(local_reader, local_writer):
    global G_vms
    while True:
        for vm in G_vms:
            if not vm.is_ready():
                continue
            print(f"serving client on {vm.imgdir}")
            await vm.serve(local_writer, local_reader)
            print(f"client on {vm.imgdir} exited.")
            return
        #no vms :(
        await asyncio.sleep(1)    




async def main():
    await initialize()

    server  = await asyncio.start_server(server_proc, '127.0.0.1', 13337)


    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    async with server:
        await server.serve_forever()



if __name__  == "__main__":
    asyncio.run(main())
    