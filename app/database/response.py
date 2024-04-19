from app.database.models import async_session, UserToken
from sqlalchemy.future import select

async def save_token(user_id, token):
    async with async_session() as session:
        new_token = UserToken(tg_id=user_id, token=token)
        session.add(new_token)
        await session.commit()

async def get_token(tg_id):
    async with async_session() as session:
        stmt = select(UserToken).where(UserToken.tg_id == tg_id)
        result = await session.execute(stmt)
        user_token = result.scalar_one_or_none()
        return user_token.token if user_token else None