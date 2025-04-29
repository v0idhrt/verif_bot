# core/ui/gender_selection_view.py

import random
import time
import logging

import discord
from discord import Interaction, Member
from discord.ui import View, button

from domain.models.verification import VerificationRequest
from core.ui.modals import RejectModal, AdditionalDataModal  # на случай, если нужны в этой вью
from domain.services.verification_service import VerificationService

log = logging.getLogger(__name__)

class GenderSelectionView(View):

    def __init__(self, service: VerificationService, target: Member, timeout: float = 60.0):
        super().__init__(timeout=timeout)
        self.service = service
        self.target = target

    @discord.ui.button(label="Мужчина", style=discord.ButtonStyle.primary)
    async def male(self, interaction: Interaction, button: discord.ui.Button):
        await self._do_verify(interaction, "male", "Мужчина")

    @discord.ui.button(label="Женщина", style=discord.ButtonStyle.primary)
    async def female(self, interaction: Interaction, button: discord.ui.Button):
        await self._do_verify(interaction, "female", "Женщина")

    async def _do_verify(self, interaction: Interaction, gender_value: str, gender_name: str):
        await interaction.response.defer(ephemeral=True)

        req = VerificationRequest(
            user_id=self.target.id,
            verifier_id=interaction.user.id,
            gender=gender_value,
            timestamp=time.time()
        )
        result = await self.service.verify_user(interaction.guild, self.target, req)

        if result.success:
            vcs = [
                vc for vc in interaction.guild.voice_channels
                if vc.permissions_for(interaction.guild.me).connect
                   and vc.permissions_for(self.target).connect
            ]
            if vcs:
                try:
                    await self.target.move_to(random.choice(vcs))
                except Exception as e:
                    log.warning("Не смогли переместить %s: %s", self.target, e)
            content = f"✅ {self.target.mention} верифицирован как **{gender_name}**"
        else:
            content = f"❌ Не удалось верифицировать: {result.reason}"

        for child in self.children:
            child.disabled = True

        await interaction.edit_original_response(content=content, view=None)

        await interaction.delete_original_response()
