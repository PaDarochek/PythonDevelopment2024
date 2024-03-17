#!/usr/bin/env python3
import asyncio
import cowsay

clients = {}
used_names = []

async def chat(reader, writer):
    receive = None
    handle = asyncio.create_task(reader.readline())
    me = ''
    quitted = False
    while not reader.at_eof():
        done, pending = None, None
        if receive is not None:
            done, pending = await asyncio.wait([handle, receive], return_when=asyncio.FIRST_COMPLETED)
        else:
            done, pending = await asyncio.wait([handle])
        for q in done:
            if q is handle:
                cmd = q.result().decode().strip().split()
                if len(cmd) == 0:
                    handle = asyncio.create_task(reader.readline())
                    continue
                if cmd[0] == 'login':
                    if me:
                        writer.write('Already logged in\n'.encode())
                        await writer.drain()
                        handle = asyncio.create_task(reader.readline())
                        continue
                    if len(cmd) != 2:
                        writer.write('Incorrect number of parameters\n'.encode())
                        await writer.drain()
                        handle = asyncio.create_task(reader.readline())
                        continue
                    name = cmd[1]
                    if name not in cowsay.list_cows():
                        writer.write('Unacceptable login. Try again\n'.encode())
                        await writer.drain()
                    elif name in used_names:
                        writer.write('This name is already in use. Try another name\n'.encode())
                        await writer.drain()
                    else:
                        me = name
                        clients[me] = asyncio.Queue()
                        receive = asyncio.create_task(clients[me].get())
                        used_names.append(name)
                        writer.write(f'Logged in as {name}\n'.encode())
                        await writer.drain()
                    handle = asyncio.create_task(reader.readline())
                    continue
                elif cmd[0] == 'who':
                    if len(cmd) != 1:
                        writer.write('Incorrect number of parameters\n'.encode())
                        await writer.drain()
                    else:
                        writer.write(f"Logged users: {', '.join(used_names)}\n".encode())
                        await writer.drain()
                    handle = asyncio.create_task(reader.readline())
                    continue
                elif cmd[0] == 'cows':
                    if len(cmd) != 1:
                        writer.write('Incorrect number of parameters\n'.encode())
                        await writer.drain()
                    else:
                        free_names = set(cowsay.list_cows()).difference(used_names)
                        writer.write(f"Free cows names: {', '.join(free_names)}\n".encode())
                        await writer.drain()
                    handle = asyncio.create_task(reader.readline())
                    continue
                elif cmd[0] == 'yield':
                    if len(cmd) < 2:
                        writer.write('Write non-empty message\n'.encode())
                        await writer.drain()
                    elif not me:
                        writer.write('You need to login before joining chat\n'.encode())
                        await writer.drain()
                    else:
                        for out in clients.values():
                            if out is not clients[me]:
                                await out.put(cowsay.cowsay(f"{me}: {' '.join(cmd[1:])}", cow=me))
                    handle = asyncio.create_task(reader.readline())
                    continue
                elif cmd[0] == 'say':
                    if len(cmd) < 3:
                        writer.write('Incorrect number of parameters: say <cow-name> <message>\n'.encode())
                        await writer.drain()
                    elif not me:
                        writer.write('You need to login before joining chat\n'.encode())
                        await writer.drain()
                    else:
                        send_name = cmd[1]
                        if send_name not in used_names:
                            writer.write(f'No user with name {send_name}\n'.encode())
                            await writer.drain()
                        else:
                            client = clients[send_name]
                            await client.put(cowsay.cowsay(f"{me}: {' '.join(cmd[2:])}", cow=me))
                    handle = asyncio.create_task(reader.readline())
                    continue
                elif cmd[0] == 'quit':
                    if len(cmd) != 1:
                        writer.write('Incorrect number of parameters\n'.encode())
                        await writer.drain()
                        handle = asyncio.create_task(reader.readline())
                        continue
                    elif not me:
                        writer.write('You need to login before quitting\n'.encode())
                        await writer.drain()
                        handle = asyncio.create_task(reader.readline())
                        continue
                    handle.cancel()
                    receive.cancel()
                    del clients[me]
                    used_names.remove(me)
                    writer.close()
                    await writer.wait_closed()
                    quitted = True
                    break
                else:
                    handle = asyncio.create_task(reader.readline())
                    continue
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
        if quitted:
            break
    if me:
        handle.cancel()
        receive.cancel()
        del clients[me]
        used_names.remove(me)
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
