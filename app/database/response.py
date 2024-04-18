from app.database.models import async_session, UserToken

async def save_token(user_id, token):
    async with async_session() as session:
        new_token = UserToken(tg_id=user_id, token=token)
        session.add(new_token)
        await session.commit()