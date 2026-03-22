from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from controllers.operator_controller import OperatorController
from controllers.conversation_controller import ConversationController
from controllers.message_controller import MessageController
from controllers.user_controller import UserController
from core.config import settings
from data_access import ConversationRepository, MessageRepository, UserRepository, OperatorRepository

router = APIRouter(prefix="/operator", tags=["operator-web"])
templates = Jinja2Templates(directory="templates")


def get_operator_controller(session=Depends(settings.get_sqlite_session)) -> OperatorController:
    return OperatorController(
        operator_repository=OperatorRepository(session),
        conversation_repository=ConversationRepository(session),
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


@router.get("/{operator_id}/profile", response_class=HTMLResponse)
def operator_profile(
    request: Request,
    operator_id: str,
    op_ctrl: OperatorController = Depends(get_operator_controller),
    user_ctrl: UserController = Depends(get_user_controller),
):
    operator = op_ctrl.get_details(operator_id)
    user = user_ctrl.get_details(operator_id)
    if user is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Operator not found. This account may have been deleted."},
            status_code=404,
        )
    return templates.TemplateResponse(
        "operator_profile.html",
        {"request": request, "operator": operator, "user": user, "operator_id": operator_id},
    )


@router.post("/{operator_id}/profile/update")
def operator_profile_update(
    operator_id: str,
    name: str = Form(...),
    email: str = Form(...),
    user_ctrl: UserController = Depends(get_user_controller),
):
    user_ctrl.update_contact_info(user_id=operator_id, name=name, email=email)
    return RedirectResponse(url=f"/operator/{operator_id}/profile", status_code=303)


@router.post("/{operator_id}/delete")
def operator_delete(
    operator_id: str,
    user_ctrl: UserController = Depends(get_user_controller),
):
    user_ctrl._user_repository.delete(operator_id)
    return RedirectResponse(url="/", status_code=303)


@router.get("/{operator_id}/conversations", response_class=HTMLResponse)
def operator_conversations(
    request: Request,
    operator_id: str,
    op_ctrl: OperatorController = Depends(get_operator_controller),
    conv_ctrl: ConversationController = Depends(get_conversation_controller),
    user_ctrl: UserController = Depends(get_user_controller),
):
    try:
        operator = op_ctrl.get_details(operator_id)
        user = user_ctrl.get_details(operator_id)
    except ValueError:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Operator not found. This account may have been deleted."},
            status_code=404,
        )
    conversations = conv_ctrl.get(operator_id=operator_id)
    unassigned_conversations = conv_ctrl.get(is_unassigned=True)
    print(unassigned_conversations)

    return templates.TemplateResponse(
        "operator_conversations.html",
        {
            "request": request,
            "operator": operator,
            "operator_id": operator_id,
            "user": user,
            "my_conversations": conversations,
            "unassigned_conversations": unassigned_conversations,
        },
    )


@router.post("/{operator_id}/conversations/{conversation_id}/assign")
def operator_assign_conversation(
    operator_id: str,
    conversation_id: str,
    op_ctrl: OperatorController = Depends(get_operator_controller),
):
    op_ctrl.assign_conversation(conversation_id=conversation_id, operator_id=operator_id)
    return RedirectResponse(url=f"/operator/{operator_id}/conversations", status_code=303)


@router.get("/{operator_id}/conversations/{conversation_id}", response_class=HTMLResponse)
def operator_conversation_detail(
    request: Request,
    operator_id: str,
    conversation_id: str,
    op_ctrl: OperatorController = Depends(get_operator_controller),
    conv_ctrl: ConversationController = Depends(get_conversation_controller),
    msg_ctrl: MessageController = Depends(get_message_controller),
    user_ctrl: UserController = Depends(get_user_controller),
):
    try:
        operator = op_ctrl.get_details(operator_id)
        user = user_ctrl.get_details(operator_id)
    except ValueError:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Operator not found. This account may have been deleted."},
            status_code=404,
        )
    conversation = conv_ctrl.get(conversation_id=conversation_id)
    client_messages = msg_ctrl.get_messages(conversation_id=conversation_id, sender_role="client")
    operator_messages = msg_ctrl.get_messages(conversation_id=conversation_id, sender_role="operator")

    return templates.TemplateResponse(
        "operator_conversation_detail.html",
        {
            "request": request,
            "operator": operator,
            "operator_id": operator_id,
            "user": user,
            "conversation": conversation,
            "client_messages": client_messages,
            "operator_messages": operator_messages,
            "viewer_role": "operator",
        },
    )


@router.post("/{operator_id}/conversations/{conversation_id}/send")
def operator_send_message(
    operator_id: str,
    conversation_id: str,
    content: str = Form(...),
    conv_ctrl: ConversationController = Depends(get_conversation_controller),
):
    conv_ctrl.add_message(conversation_id=conversation_id, content=content, sender_role="operator")
    return RedirectResponse(
        url=f"/operator/{operator_id}/conversations/{conversation_id}",
        status_code=303,
    )


@router.post("/{operator_id}/conversations/{conversation_id}/resolve")
def operator_resolve_conversation(
    operator_id: str,
    conversation_id: str,
    op_ctrl: OperatorController = Depends(get_operator_controller),
):
    op_ctrl.resolve_conversation(conversation_id=conversation_id)
    return RedirectResponse(url=f"/operator/{operator_id}/conversations", status_code=303)