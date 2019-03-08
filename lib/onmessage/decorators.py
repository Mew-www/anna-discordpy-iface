from functools import wraps
from asyncio import iscoroutinefunction


def on_content_start(beginning, prefix=""):
    """
    :param beginning: Beginning of content (after prefix).
    :param prefix: Prefix before beginning (if any).
    """

    def decorator(func):

        @wraps(func)
        def _wrapper(msg, *args, **kwargs):
            if msg.content.startswith('{}{}'.format(prefix, beginning)):
                return func(msg, *args, **kwargs)

        @wraps(func)
        async def _async_wrapper(msg, *args, **kwargs):
            if msg.content.startswith('{}{}'.format(prefix, beginning)):
                return await func(msg, *args, **kwargs)

        if iscoroutinefunction(func):
            return _async_wrapper
        else:
            return _wrapper

    return decorator


def on_authors(users):
    """
    :param users: List of permitted Name#NNNN -tags.
    """

    def decorator(func):
        @wraps(func)
        def _wrapper(msg, *args, **kwargs):
            if '{}#{}'.format(msg.author.name, msg.author.discriminator) in users:
                return func(msg, *args, **kwargs)

        @wraps(func)
        async def _async_wrapper(msg, *args, **kwargs):
            if '{}#{}'.format(msg.author.name, msg.author.discriminator) in users:
                return await func(msg, *args, **kwargs)

        if iscoroutinefunction(func):
            return _async_wrapper
        else:
            return _wrapper

    return decorator


def on_server(name=None, owner=None):
    """
    :param name: Current server name.
    :param owner: Name#NNNN -tag of server owner.
    """

    if name is None and owner is None:
        raise ValueError('Either (server) name or (server) owner is required')

    def decorator(func):

        @wraps(func)
        def _wrapper(msg, *args, **kwargs):
            if name is not None and name == msg.server.name:
                return func(msg, *args, **kwargs)
            elif owner is not None and owner == '{}#{}'.format(msg.server.owner.name, msg.server.owner.discriminator):
                return func(msg, *args, **kwargs)

        @wraps(func)
        async def _async_wrapper(msg, *args, **kwargs):
            if name is not None and name == msg.server.name:
                return await func(msg, *args, **kwargs)
            elif owner is not None and owner == '{}#{}'.format(msg.server.owner.name, msg.server.owner.discriminator):
                return await func(msg, *args, **kwargs)

        if iscoroutinefunction(func):
            return _async_wrapper
        else:
            return _wrapper

    return decorator
