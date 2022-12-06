from datetime import datetime
import os

from dotenv import load_dotenv

import asyncpg
from schemas import User, Message, Chat

load_dotenv()
DB_URL = os.environ['DB_URL']


async def get_user_by_id(con_pool, user_id: int) -> User | None:
    async with con_pool.acquire() as conn:
        user = await conn.fetchrow(
            'select * from "user" where id=$1', user_id
        )
        return User(**dict(user)) if user else None


async def get_user_by_username(con_pool, username: str) -> User | None:
    async with con_pool.acquire() as conn:
        user = await conn.fetchrow(
            'select * from "user" where username=$1', username
        )
        return User(**dict(user)) if user else None


async def get_users(con_pool, contains: str) -> list[User]:
    async with con_pool.acquire() as conn:
        return [User(**dict(u)) for u in
                await conn.fetch('select * from "user" where username like $1', f'%{contains}%')]


async def create_user(con_pool, username: str, hashed_password) -> User | None:
    async with con_pool.acquire() as conn:
        try:
            user_id = await conn.fetchval(
                'insert into "user"(username, hashed_password) values ($1, $2) returning id', username, hashed_password
            )
        except Exception:
            return None
        return User(id=user_id, username=username, hashed_password=hashed_password)


async def get_or_create_chat(con_pool, user_id1: int, user_id2: int) -> Chat | None:
    async with con_pool.acquire() as conn:
        chat = await conn.fetchrow(
            'select * from chat where (user_id1=$1 and user_id2=$2) or (user_id1=$2 and user_id2=$1)', user_id1,
            user_id2
        )
        if chat:
            return Chat(**dict(chat))
        else:
            try:
                chat_id = await conn.fetchval(
                    'insert into chat(user_id1, user_id2) values ($1, $2) returning id', user_id1, user_id2
                )
                return Chat(id=chat_id, user_id1=user_id1, user_id2=user_id2)
            except Exception:
                return None


async def user_in_chat(con_pool, chat_id: int, user_id: int) -> bool:
    async with con_pool.acquire() as conn:
        chat = await conn.fetchrow(
            'select * from chat where id=$1 and (user_id1 = $2 or user_id2 = $2)', chat_id, user_id
        )
        return bool(chat)


async def create_message(con_pool, chat_id: int, user_id: int, content: str) -> Message | None:
    async with con_pool.acquire() as conn:
        created = datetime.now()
        try:
            message_id = await conn.fetchval(
                'insert into message(user_id, chat_id, created, content) values ($1, $2, $3, $4) returning id',
                user_id, chat_id, created, content
            )
            return Message(id=message_id, chat_id=chat_id, user_id=user_id, content=content, created=created)
        except Exception:
            return None


async def get_messages(con_pool, chat_id: int) -> list[Message]:
    async with con_pool.acquire() as conn:
        messages = await conn.fetch(
            'select * from message where chat_id = $1', chat_id
        )
        return [Message(**dict(m)) for m in messages]


async def get_pool():
    return await asyncpg.create_pool(DB_URL)


if __name__ == '__main__':
    pass
