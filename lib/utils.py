import asyncio
import aiohttp


# A background task to be alive
async def be_alive(anna):
    await anna.wait_until_ready()
    while True:
        await asyncio.sleep(1)


# A blocking function to exit gracefully if must
def gracefully_exit_discord(anna):
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
        except aiohttp.errors.ClientResponseError:
            pass
        except ConnectionResetError:
            pass
