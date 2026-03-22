from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from controllers import UserController
from controllers.client_controller import ClientController
from controllers.conversation_controller import ConversationController
from controllers.message_controller import MessageController
from core.config import settings
from data_access import ConversationRepository, MessageRepository, ClientRepository, UserRepository

router = APIRouter(prefix="/client", tags=["client-web"])
templates = Jinja2Templates(directory="templates")


def get_client_controller(session=Depends(settings.get_sqlite_session)) -> ClientController:
    return ClientController(
        client_repository=ClientRepository(session),
        conversation_repository=ConversationRepository(session),
        message_repository=MessageRepository(session),
        user_repository=UserRepository(session),
    )


def get_conversation_controller(session=Depends(settings.get_sqlite_session)) -> ConversationController:
    return ConversationController(
        conversation_repository=ConversationRepository(session),
        message_repository=MessageRepository(session),
    )


def get_message_controller(session=Depends(settings.get_sqlite_session)) -> MessageController:
    return MessageController(message_repository=MessageRepository(session))


def get_user_controller(session=Depends(settings.get_sqlite_session)) -> UserController:
    return UserController(user_repository=UserRepository(session))


@router.get("/{client_id}/conversations", response_class=HTMLResponse)
def client_conversations(
    request: Request,
    client_id: str,
    client_ctrl: ClientController = Depends(get_client_controller),
    conv_ctrl: ConversationController = Depends(get_conversation_controller),
    user_ctrl: UserController = Depends(get_user_controller),
):
    client = client_ctrl.get_details(client_id=client_id)
    user = user_ctrl.get_details(user_id=client_id)
    if client is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Client not found. This account may have been deleted."},
            status_code=404,
        )
    conversations = conv_ctrl.get(client_id=client_id)
    return templates.TemplateResponse(
        "client_conversations.html",
        {"request": request, "client": client, "user": user, "conversations": conversations},
    )


@router.post("/{client_id}/conversations/new")
def client_create_conversation(
    client_id: str,
    priority: str = Form(...),
    client_ctrl: ClientController = Depends(get_client_controller),
):
    client_ctrl.initiate_conversation(
        client_id=client_id,
        priority=priority,
    )
    return RedirectResponse(url=f"/client/{client_id}/conversations", status_code=303)


@router.get("/{client_id}/conversations/{conversation_id}", response_class=HTMLResponse)
def client_conversation_detail(
    request: Request,
    client_id: str,
    conversation_id: str,
    client_ctrl: ClientController = Depends(get_client_controller),
    conv_ctrl: ConversationController = Depends(get_conversation_controller),
    msg_ctrl: MessageController = Depends(get_message_controller),
    user_ctrl: UserController = Depends(get_user_controller),
):
    client = client_ctrl.get_details(client_id=client_id)
    user = user_ctrl.get_details(user_id=client_id)
    if client is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Client not found. This account may have been deleted."},
            status_code=404,
        )
    conversation = conv_ctrl.get(conversation_id=conversation_id)
    client_messages = msg_ctrl.get_messages(conversation_id=conversation_id, sender_role="client")
    operator_messages = msg_ctrl.get_messages(conversation_id=conversation_id, sender_role="operator")

    return templates.TemplateResponse(
        "client_conversation_detail.html",
        {
            "request": request,
            "client": client,
            "user": user,
            "conversation": conversation,
            "client_messages": client_messages,
            "operator_messages": operator_messages,
            "viewer_role": "client",
        },
    )


@router.post("/{client_id}/conversations/{conversation_id}/send")
def client_send_message(
    client_id: str,
    conversation_id: str,
    content: str = Form(...),
    client_ctrl: ClientController = Depends(get_client_controller),
):
    client_ctrl.submit_feedback(
        client_id=client_id,
        conversation_id=conversation_id,
        content=content,
    )
    return RedirectResponse(
        url=f"/client/{client_id}/conversations/{conversation_id}",
        status_code=303,
    )


@router.get("/{client_id}/profile", response_class=HTMLResponse)
def client_profile(
    request: Request,
    client_id: str,
    client_ctrl: ClientController = Depends(get_client_controller),
    user_ctrl: UserController = Depends(get_user_controller),
):
    client = client_ctrl.get_details(client_id=client_id)
    user = user_ctrl.get_details(user_id=client_id)
    if client is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Client not found. This account may have been deleted."},
            status_code=404,
        )
    return templates.TemplateResponse(
        "client_profile.html",
        {"request": request, "client": client, "user": user},
    )


@router.post("/{client_id}/profile/update")
def client_profile_update(
    client_id: str,
    name: str = Form(...),
    email: str = Form(...),
    user_ctrl: UserController = Depends(get_user_controller),
):
    user_ctrl.update_contact_info(user_id=client_id, name=name, email=email)
    return RedirectResponse(url=f"/client/{client_id}/profile", status_code=303)


@router.post("/{client_id}/delete")
def client_delete(
    client_id: str,
    client_ctrl: ClientController = Depends(get_client_controller),
):
    client_ctrl.delete_client(client_id)
    return RedirectResponse(url="/", status_code=303)