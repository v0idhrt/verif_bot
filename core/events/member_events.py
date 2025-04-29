from discord.ext import commands
from discord import Member
from config import settings

class MemberEvents(commands.Cog):
    def __init__(self, unverified_role_id: int):
        self.unverified_role_id = unverified_role_id

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        role = member.guild.get_role(self.unverified_role_id)
        if role:
            await member.add_roles(role, reason="Automatic unverified on join")


async def setup_member_events(bot: commands.Bot):
    await bot.add_cog(MemberEvents(settings.unverified_role_id))
