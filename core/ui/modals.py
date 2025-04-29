import logging
import discord
from discord import Interaction, Member
from discord.ui import Modal, TextInput

log = logging.getLogger(__name__)

class RejectModal(Modal):
    def __init__(self, target: Member):
        super().__init__(title="Причина отказа")
        self.target = target
        self.reason = TextInput(label="Причина отказа", style=discord.TextStyle.paragraph, required=True)
        self.add_item(self.reason)

    async def on_submit(self, interaction: Interaction):
        try:
            await self.target.kick(reason=self.reason.value)
            content = f"❌ {self.target.mention} кикнут. Причина: {self.reason.value}"
        except Exception as e:
            log.exception("kick failed")
            content = f"❌ Не удалось кикнуть: {e}"
        await interaction.response.send_message(content, ephemeral=True)


class AdditionalDataModal(Modal):
    def __init__(self, target: Member):
        super().__init__(title="Дополнительные данные")
        self.target = target
        self.twink = TextInput(label="Твинк? (да/нет)", style=discord.TextStyle.short, required=True)
        self.owner = TextInput(label="Владелец аккаунта", style=discord.TextStyle.short, required=False)
        self.add_item(self.twink)
        self.add_item(self.owner)

    async def on_submit(self, interaction: Interaction):
        content = (
            f"💾 Доп. данные по {self.target.mention}:\n"
            f"• Твинк: {self.twink.value}\n"
            f"• Владелец: {self.owner.value or 'Не указан'}"
        )
        await interaction.response.send_message(content, ephemeral=True)
