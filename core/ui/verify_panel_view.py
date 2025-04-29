import logging, random, time
import discord
from discord import Interaction, Member
from discord.ui import View

from core.ui.modals import RejectModal, AdditionalDataModal
from core.ui.change_gender_view import ChangeGenderView
from core.ui.gender_selection_view import GenderSelectionView
from domain.services.verification_service import VerificationService

log = logging.getLogger(__name__)

class UnverifiedView(View):
    def __init__(self, service: VerificationService, target: Member):
        super().__init__(timeout=120)
        self.service = service
        self.target = target

    @discord.ui.button(label="Вериф", style=discord.ButtonStyle.primary)
    async def verify_button(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            view=GenderSelectionView(self.service, self.target)
        )

    @discord.ui.button(label="Отклонить", style=discord.ButtonStyle.danger)
    async def reject_button(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RejectModal(self.target))


class VerifiedView(View):
    def __init__(self, service: VerificationService, target: Member):
        super().__init__(timeout=120)
        self.service = service
        self.target = target

    @discord.ui.button(label="Сменить гендер", style=discord.ButtonStyle.secondary)
    async def change_gender_button(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Выберите новый гендер:", 
            view=ChangeGenderView(self.service, self.target),
            ephemeral=True
        )

    @discord.ui.button(label="Доп. данные", style=discord.ButtonStyle.success)
    async def additional_data_button(self, interaction: Interaction, button: discord.ui.Button):
        # Модалка с твинком/владельцем
        await interaction.response.send_modal(AdditionalDataModal(self.target))
