#!/usr/bin/env python3
import discord
import os
import asyncio
from lib.voice.espeak_voicebox import ESpeakVoicebox
from lib.voice.voicebuffer import VoiceBuffer
from lib.onmessage.administrative_handlers import handle_changename
from lib.onmessage.administrative_handlers import handle_voicejoin, handle_speaking, handle_voiceleave, handle_setvoice
from lib.onmessage.common_handlers import handle_hello
from lib.onmember.administrative_handlers import handle_jorans_new_member


def main():
    print('Discord client starting')
    anna = discord.Client(max_messages=1000)
    voicebox = ESpeakVoicebox()
    voicebuffer = VoiceBuffer(anna, voicebox)  # Essentially "Controller"; Buffers and relays requests to speak

    # A background task to be alive
    async def task():
        await anna.wait_until_ready()
        while True:
            await asyncio.sleep(1)

    # A blocking function to exit gracefully if must
    def handle_exit():
        print("Exiting Discord..")
        anna.loop.run_until_complete(anna.logout())
        for t in asyncio.Task.all_tasks(loop=anna.loop):
            if t.done():
                t.exception()
                continue
            t.cancel()
            try:
                anna.loop.run_until_complete(asyncio.wait_for(t, 5, loop=anna.loop))
                t.exception()
            except asyncio.InvalidStateError:
                pass
            except asyncio.TimeoutError:
                pass
            except asyncio.CancelledError:
                pass

    while True:

        # Event Handlers

        @anna.event
        async def on_ready():
            servers = ', '.join(list('"{}"'.format(s.name) for s in anna.servers))
            print('Connected to Discord as {}#{} on {}'.format(anna.user.name, anna.user.discriminator, servers))

        @anna.event
        async def on_server_join(server):
            print('Joined server {}'.format(server.name))

        @anna.event
        async def on_server_remove(server):
            print('Vacated from server {}'.format(server.name))

        @anna.event
        async def on_message(msg):
            await handle_changename(msg, anna)
            await handle_hello(msg, anna)
            await handle_voicejoin(msg, anna, voicebuffer)
            await handle_speaking(msg, anna, voicebuffer)
            await handle_voiceleave(msg, anna, voicebuffer)
            await handle_setvoice(msg, anna, voicebox)

        @anna.event
        async def on_member_join(member):
            await handle_jorans_new_member(member, anna)

        anna.loop.create_task(task())
        try:
            anna.loop.run_until_complete(anna.start(os.environ['DISCORD_BOT_CLIENT_SECRET_TOKEN']))
        except SystemExit:
            handle_exit()
        except KeyboardInterrupt:
            handle_exit()
            anna.loop.close()
            print('Manually exited.')
            break

        print('Restarting after a graceful exit.')
        anna = discord.Client(loop=anna.loop)


if __name__ == "__main__":
    main()
