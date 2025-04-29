import discord
from discord import app_commands, Interaction, Member
from discord.ext import commands
from discord.app_commands import check, describe

from config import settings
from core.ui.verify_panel_view import UnverifiedView, VerifiedView
from domain.services.verification_service import VerificationService

GUILD_ID       = settings.guild_id
SUPPORT_ROLE_ID = settings.support_role_id

def is_support():
    return check(lambda i: SUPPORT_ROLE_ID in [r.id for r in i.user.roles])

class VerifyPanelCommand(commands.Cog):
    def __init__(self, bot: commands.Bot, service: VerificationService):
        self.bot     = bot
        self.service = service

    @app_commands.command(
        name="action",
        description="Открыть панель действий для указанного пользователя"
    )
    @app_commands.guilds(GUILD_ID)
    @is_support()
    @describe(user="Кого проверить")
    async def verify_panel(self, interaction: Interaction, user: Member):

        has_gender = any(
            role.id in self.service.gender_roles.values()
            for role in user.roles
        )

        embed = discord.Embed(
            title="Панель верификации",
            description=f"{user.mention}",
            type="rich",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="Дата регистрации", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Юзернейм", value=str(user), inline=False)

        view = VerifiedView(self.service, user) if has_gender \
               else UnverifiedView(self.service, user)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot: commands.Bot, service: VerificationService):
    await bot.add_cog(VerifyPanelCommand(bot, service))
