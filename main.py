# Python 3.9 is required
from signalextract import signals
import asyncio
import logging

from asyncua import Server, ua

#Extrae las señales desde el excel 
signals = signals()
folders=signals['Folder'].unique()

async def main():
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name('CIRCE')

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # populating our address space
    
    for folder in folders:
        globals()[f'Temp_{folder}'] = await server.nodes.objects.add_folder(idx,folder)
        temp_signals=signals[signals.Folder==folder]
        nodes = temp_signals['Node'].unique()
        for node in nodes:
            globals()[f'Temp_{node}'] = await globals()[f'Temp_{folder}'].add_object(idx, node)
            temp_tags=temp_signals[temp_signals.Node==node]
            tags=temp_tags['Tag'].unique()
            for tag in tags:
                globals()[f'Temp_{tag}'] = await globals()[f'Temp_{node}'].add_variable(idx, tag, 0.0)
                await globals()[f'Temp_{tag}'].set_writable()

    async with server:
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(), debug=False)
