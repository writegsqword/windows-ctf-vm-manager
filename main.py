import asyncio
import vminstance
from vminstance import VMInstance
import os




G_vms: list[VMInstance] = []
VM_IMG = os.path.abspath("./vm/img")
VM_WORKDIR = os.path.abspath("./vm/working")


async def initialize():
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
            vm.serve(local_writer, local_reader)
            return
        #no vms :(
        asyncio.sleep(1)    







if __name__  == "__main__":
    # Create the server
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(server_proc, '127.0.0.1', 13337)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()