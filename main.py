from fastapi import FastAPI, Depends, Request, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth import authenticate_user, create_access_token, get_current_user, get_websocket_user
from schemas import Chat, Message, Token, UserOut
from ws_manager import ConnectionManager
import db

app = FastAPI()
app.mount('/assets', StaticFiles(directory='./frontend_web/dist/assets'), name='static')

templates = Jinja2Templates(directory='./frontend_web/dist')

manager = ConnectionManager()


@app.get('/')
async def serve_spa(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.on_event('startup')
async def init_app():
    app.state.pool = await db.get_pool()


@app.on_event('shutdown')
async def close_app():
    await app.state.pool.close()


@app.post('/token', response_model=Token)
async def get_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    pool = request.app.state.pool
    user = await authenticate_user(pool, form_data.username, form_data.password)
    access_token = create_access_token({'sub': user.username})
    return Token(access_token=access_token, token_type='bearer')


@app.post('/create_chat', response_model=Chat)
async def create_chat(request: Request, user_id: int, user=Depends(get_current_user)):
    pool = request.app.state.pool
    chat = await db.get_or_create_chat(pool, user.id, user_id)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await db.get_or_create_chat(pool, user.id, user_id)


@app.get('/messages', response_model=list[Message])
async def messages(request: Request, chat_id: int, user=Depends(get_current_user)):
    pool = request.app.state.pool
    if not await db.user_in_chat(pool, chat_id, user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await db.get_messages(pool, chat_id)


@app.get('/me', response_model=UserOut)
async def me(user=Depends(get_current_user)):
    return UserOut(**dict(user))


@app.get('/users', dependencies=[Depends(get_current_user)], response_model=list[UserOut])
async def users(request: Request, q: str = ''):
    pool = request.app.state.pool
    return await db.get_users(pool, q)


@app.websocket('/messenger')
async def messenger(websocket: WebSocket, chat_id: int, user=Depends(get_websocket_user)):
    pool = websocket.app.state.pool
    if not await db.user_in_chat(pool, chat_id, user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await manager.connect(websocket, chat_id)
    try:
        while True:
            text = await websocket.receive_text()
            message = await db.create_message(pool, chat_id, user.id, text)
            if not message:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            await manager.send_message(message, chat_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)
