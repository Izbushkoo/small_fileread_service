from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from jinja_process.base import example_equation, example_first_type, example_second_type


examples_router = APIRouter()


@examples_router.get("/equation_card")
async def example_equation_card():
    """Посмотреть как будет """

    return HTMLResponse(example_equation())


@examples_router.get("/first")
async def example_first():
    """Посмотреть как будет """
    return HTMLResponse(example_first_type())


@examples_router.get("/second")
async def example_second():
    """Посмотреть как будет """
    return HTMLResponse(example_second_type())
