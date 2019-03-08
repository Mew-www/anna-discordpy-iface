#!/usr/bin/env python3
import discord
import os


def main():
    print('Discord client starting')
    anna = discord.Client(max_messages=1000)

    @anna.event
    async def on_ready():
        print('Connected to Discord as {}#{}'.format(anna.user.name, anna.user.discriminator))
        print('Resuming on servers: {}'.format(', '.join(list('"{}"'.format(s.name) for s in anna.servers))))

    @anna.event
    async def on_server_join(server):
        print('Joined server {}'.format(server.name))

    @anna.event
    async def on_server_remove(server):
        print('Vacated from server {}'.format(server.name))

    @anna.event
    async def on_message(msg):
        pass

    anna.run(os.environ['DISCORD_BOT_CLIENT_SECRET_TOKEN'])


if __name__ == "__main__":
    main()
