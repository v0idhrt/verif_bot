from db.connection import DB
from datetime import datetime
import json

async def log_action(moderator_id: int, target_id: int, action: str, details: dict | None = None):
    async with DB.pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO support_logs (timestamp, moderator_id, target_id, action, details)
            VALUES ($1, $2, $3, $4, $5)
        """, datetime.now(), moderator_id, target_id, action, json.dumps(details) if details else None)
