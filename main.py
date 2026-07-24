from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from supabase_client import supabase

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Temporary storage (for demo only)
user_data = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/payment")
async def payment(
    request: Request,
    name: str = Form(...),
    phone: str = Form(...)
):

    phone = phone.strip()

    if not phone.isdigit() or len(phone) != 10:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": "Please enter a valid 10-digit mobile number."
            },
            status_code=400
        )

    user_data["name"] = name
    user_data["phone"] = phone

    return templates.TemplateResponse(
        request=request,
        name="payment.html"
    )


@app.get("/amount", response_class=HTMLResponse)
async def amount(request: Request):

    return templates.TemplateResponse(
            request=request,
            name="amount.html"
        )


@app.post("/submit")
async def submit(
    request: Request,
    amount: float = Form(...)
):

    supabase.table("donations").insert({
        "name": user_data["name"],
        "phone": user_data["phone"],
        "amount": amount
    }).execute()

    return templates.TemplateResponse(
                request=request,
                name="success.html"
            )