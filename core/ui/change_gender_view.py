# core/ui/change_gender_view.py

import asyncio
import discord
from discord import Interaction, Member
from discord.ui import View, button

from domain.services.verification_service import VerificationService

class ChangeGenderView(View):
    def __init__(self, service: VerificationService, target: Member, timeout: float = 60.0):
        super().__init__(timeout=timeout)
        self.service = service
        self.target = target

    @button(label="Мужчина", style=discord.ButtonStyle.primary)
    async def male(self, interaction: Interaction, button: discord.ui.Button):
        await self._do_change(interaction, "male", "Мужчина")

    @button(label="Женщина", style=discord.ButtonStyle.primary)
    async def female(self, interaction: Interaction, button: discord.ui.Button):
        await self._do_change(interaction, "female", "Женщина")

    async def _do_change(self, interaction: Interaction, gender_value: str, gender_name: str):
        await interaction.response.defer(ephemeral=True)

        result = await self.service.change_gender_user(
            interaction.guild, self.target, gender_value
        )

        content = (
            f"🔄 {self.target.mention} гендер изменён на **{gender_name}**"
            if result.success else f"❌ Ошибка: {result.reason}"
        )
        message = await interaction.followup.send(content=content, ephemeral=True)
        await asyncio.sleep(2)
        await message.delete()

        for child in self.children:
            child.disabled = True

        await interaction.delete_original_response()
