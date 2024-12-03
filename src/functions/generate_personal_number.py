from sqlalchemy.ext.asyncio import AsyncSession
from models import Branch

# Генерация номера учасника 
async def generate_personal_number(session: AsyncSession, branch_id: int, code: str):
        branch = await session.get(Branch, branch_id)
        personal_number = (f"{branch.code + code}")
        return personal_number