from discord import ChannelType


async def handle_jorans_new_member(member, anna):
    DEFAULT_ROLE_NAME = 'Steffen\'s Crustaceans'
    if '{}#{}'.format(member.server.owner.name, member.server.owner.discriminator) == 'Joran#3781':
        # Ensure a channel is available
        available_channels = [ch for ch in member.server.channels
                              if 'rules' not in ch.name and ch.type == ChannelType.text]
        if not available_channels:
            return
        else:
            announce_channel = available_channels[0]
        # Ensure default role is known
        matching_roles = [role for role in member.server.roles if role.name == DEFAULT_ROLE_NAME]
        if not matching_roles:
            await anna.send_message(announce_channel, 'Default role has changed from {}'.format(DEFAULT_ROLE_NAME))
            return
        else:
            default_role = matching_roles[0]
        await anna.add_roles(member, default_role)
        await anna.send_message(announce_channel, '*KSKSKSKSKSKS*')
