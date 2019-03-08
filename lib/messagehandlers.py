from .messagedecorators import on_content_start, on_authors, on_server
import os
from bs4 import BeautifulSoup, NavigableString
import requests
import random


command_prefix = os.environ['DISCORD_BOT_PREFIX']
administrative_users = os.environ['DISCORD_ADMINISTRATIVE_USERTAGS'].split(',')


@on_content_start("changename", prefix=command_prefix)
@on_authors(administrative_users)
async def handle_changename(message, anna):
    # Fetch names
    soup = BeautifulSoup(requests.get('https://en.wikipedia.org/wiki/Anna_(given_name)').text, 'html.parser')
    content = soup.find('div', {'class': "mw-parser-output"})
    names_countries = []
    for content_child in content.children:
        if not isinstance(content_child, NavigableString) and content_child.name == 'ul':
            for list_child in content_child.children:
                if not isinstance(list_child, NavigableString):
                    name_country = list_child.text.split(u'\u2013')
                    if len(name_country) < 2:
                        name_country = list_child.text.split(u'\u002D')
                    name_country[0] = name_country[0].strip()
                    name_country[1] = list(map(lambda country: country.strip(), name_country[1].split(',')))
                    names_countries.append(name_country)
            break
    # Pick one
    new_alias = random.choice(names_countries)
    await anna.change_nickname(message.server.me, new_alias[0])
    await anna.send_message(message.channel, 'Of {} origin.'.format('/'.join(new_alias[1])))


@on_content_start("hello", prefix=command_prefix)
async def handle_hello(message, anna):
    greetings = ['Goeie dag', 'Tungjatjeta', 'Ahlan bik', 'Nomoskar', 'Selam', 'Mingala ba', 'Nín hao', 'Zdravo',
                 'Nazdar', 'Hallo', 'Rush B', 'Helo', 'Hei', 'Bonjour', 'Guten Tag', 'Geia!', 'Shalóm', 'Namasté',
                 'Szia', 'Hai', 'Kiana', 'Dia is muire dhuit', 'Buongiorno', 'Kónnichi wa', 'Annyeonghaseyo',
                 'Sabai dii', 'Ave', 'Es mīlu tevi', 'Selamat petang', 'sain baina uu', 'Namaste', 'Hallo.', 'Salâm',
                 'Witajcie', 'Olá', 'Salut', 'Privét', 'Talofa', 'ćao', 'Nazdar', 'Zdravo', 'Hola', 'Jambo', 'Hej',
                 'Halo', 'Sàwàtdee kráp', 'Merhaba', 'Pryvít', 'Adaab arz hai', 'Chào']
    await anna.send_message(message.channel, random.choice(greetings))
