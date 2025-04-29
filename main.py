# main.py

import discord
from discord.ext import commands
from discord import Object
import logging

from config import settings
from domain.services.verification_service import VerificationService
from core.commands.verify_panel import setup as setup_verify
from core.events.member_events import setup_member_events

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("verifbot")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

GUILD = Object(id=settings.guild_id)

class VerifBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",  # не важно, слеш‑команды
            intents=intents
        )
        self.verification_service = VerificationService(
            {"male": settings.male_role_id, "female": settings.female_role_id},
            settings.unverified_role_id
        )

    async def setup_hook(self):
        log.info("🔧 setup_hook: регистрируем Cogs и синхронизируем команды")
        await setup_verify(self, self.verification_service)
        await setup_member_events(self)
        synced = await self.tree.sync(guild=GUILD)
        log.info("✅ Synced commands for guild %s: %s", GUILD.id, [c.name for c in synced])

    async def on_ready(self):
        log.info("🚀 Logged in as %s (ID: %s)", self.user, self.user.id)

if __name__ == "__main__":
    bot = VerifBot()
    log.info("🟢 Starting bot…")
    bot.run(settings.discord_token)
    log.info("🛑 Bot has stopped")
