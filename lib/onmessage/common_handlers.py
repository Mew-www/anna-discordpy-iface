from .decorators import on_content_start
import os
import random


command_prefix = os.environ['DISCORD_BOT_PREFIX']


@on_content_start("hello", prefix=command_prefix)
async def handle_hello(message, anna):
    greetings = ['Goeie dag', 'Tungjatjeta', 'Ahlan bik', 'Nomoskar', 'Selam', 'Mingala ba', 'Nín hao', 'Zdravo',
                 'Nazdar', 'Hallo', 'Rush B', 'Helo', 'Hei', 'Bonjour', 'Guten Tag', 'Geia!', 'Shalóm', 'Namasté',
                 'Szia', 'Hai', 'Kiana', 'Dia is muire dhuit', 'Buongiorno', 'Kónnichi wa', 'Annyeonghaseyo',
                 'Sabai dii', 'Ave', 'Es mīlu tevi', 'Selamat petang', 'sain baina uu', 'Namaste', 'Hallo.', 'Salâm',
                 'Witajcie', 'Olá', 'Salut', 'Privét', 'Talofa', 'ćao', 'Nazdar', 'Zdravo', 'Hola', 'Jambo', 'Hej',
                 'Halo', 'Sàwàtdee kráp', 'Merhaba', 'Pryvít', 'Adaab arz hai', 'Chào']
    await anna.send_message(message.channel, random.choice(greetings))
