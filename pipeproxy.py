import asyncio 

#thank 2 https://stackoverflow.com/questions/46413879/how-to-create-tcp-proxy-server-with-asyncio


async def pipe(reader, writer):
    try:
        while not reader.at_eof():
            writer.write(await reader.read(2048))
    finally:
        writer.close()



async def handle_client(local_reader, local_writer, remote_reader, remote_writer):
    try:
        pipe1 = pipe(local_reader, remote_writer)
        pipe2 = pipe(remote_reader, local_writer)
        await asyncio.gather(pipe1, pipe2)
    finally:
        local_writer.close()



    

