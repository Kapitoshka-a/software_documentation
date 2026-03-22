from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from controllers import UserController, OperatorController, ClientController
from core.errors import EntityNotFoundError
from routers.client_web import get_client_controller
from routers.operator_web import get_user_controller, get_operator_controller

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=["home-web"])

STATIC_PASSWORD = "pass"


@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": ""})


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    user_controller: UserController = Depends(get_user_controller),
    operator_controller: OperatorController = Depends(get_operator_controller),
    client_controller: ClientController = Depends(get_client_controller),
):
    if password != STATIC_PASSWORD:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Incorrect password."},
            status_code=401,
        )

    if (user := user_controller.get_details(name=username)) is None:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": f"No user found with name '{username}'."},
            status_code=401,
        )

    if operator_controller.get_details(operator_id=user.id):
        return RedirectResponse(url=f"/operator/{user.id}/conversations", status_code=303)

    if client_controller.get_details(client_id=user.id):
        return RedirectResponse(url=f"/client/{user.id}/conversations", status_code=303)


    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "User has no client or operator role assigned."},
        status_code=401,
    )