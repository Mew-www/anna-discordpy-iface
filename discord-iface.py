#!/usr/bin/env python3
import discord
import os
from lib.onmessage.administrative_handlers import handle_changename
from lib.onmessage.common_handlers import handle_hello


def main():
    print('Discord client starting')
    anna = discord.Client(max_messages=1000)

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

    anna.run(os.environ['DISCORD_BOT_CLIENT_SECRET_TOKEN'])


if __name__ == "__main__":
    main()
