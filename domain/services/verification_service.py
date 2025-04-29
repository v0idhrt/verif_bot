from discord import Guild, Member
from domain.models.verification import VerificationRequest, VerificationResult

class VerificationService:
    def __init__(self, gender_roles: dict[str, int], unverified_role_id: int):
        self.gender_roles = gender_roles
        self.unverified_role_id = unverified_role_id

    async def verify_user(
        self, guild: Guild, user: Member, data: VerificationRequest
    ) -> VerificationResult:
        try:
            # 1) Снимаем все старые гендер‑роли, чтобы не было двух сразу
            for rid in self.gender_roles.values():
                r = guild.get_role(rid)
                if r and r in user.roles:
                    await user.remove_roles(r)
            # 2) Снимаем Unverified
            uv = guild.get_role(self.unverified_role_id)
            if uv and uv in user.roles:
                await user.remove_roles(uv)
            # 3) Выдаём новую гендер‑роль
            gr = guild.get_role(self.gender_roles[data.gender])
            await user.add_roles(gr)
            return VerificationResult(user_id=user.id, success=True, reason="OK")
        except Exception as e:
            return VerificationResult(user_id=user.id, success=False, reason=str(e))

    async def unverify_user(
        self, guild: Guild, user: Member, reason: str
    ) -> VerificationResult:
        try:
            # Снимаем все гендер‑роли
            for rid in self.gender_roles.values():
                r = guild.get_role(rid)
                if r and r in user.roles:
                    await user.remove_roles(r)
            # Выдаём Unverified
            uv = guild.get_role(self.unverified_role_id)
            if uv:
                await user.add_roles(uv)
            return VerificationResult(user_id=user.id, success=True, reason=reason)
        except Exception as e:
            return VerificationResult(user_id=user.id, success=False, reason=str(e))

    async def change_gender_user(
        self, guild: Guild, user: Member, new_gender: str
    ) -> VerificationResult:
        try:
            # 🔄 Принудительно обновляем данные пользователя (из API, не из кэша)
            user = await guild.fetch_member(user.id)

            target_id = self.gender_roles[new_gender]
            target_role = guild.get_role(target_id)

            # ✅ Проверка на уже существующую роль
            if target_role in user.roles:
                return VerificationResult(
                    user_id=user.id,
                    success=False,
                    reason="У пользователя уже установлена эта роль"
                )

            # 🔁 Удаляем старые гендерные роли
            for rid in self.gender_roles.values():
                r = guild.get_role(rid)
                if r and r in user.roles:
                    await user.remove_roles(r)

            # ➕ Добавляем новую
            await user.add_roles(target_role)

            return VerificationResult(user_id=user.id, success=True, reason="OK")

        except Exception as e:
            return VerificationResult(user_id=user.id, success=False, reason=str(e))

