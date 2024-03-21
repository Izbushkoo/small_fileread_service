import csv
import io
import uuid
from typing import List, Dict, Literal
from fastapi import APIRouter, UploadFile, HTTPException, Response

from jinja_process.utils import CSVHandler
from jinja_process.base import templates_handler_factory


card_router = APIRouter()


def prepare_csv_to_response(data: List[List], filename: str) -> Response:
    buffer = io.StringIO()
    csv_writer = csv.writer(buffer)
    for row in data:
        csv_writer.writerow(row)
    response = Response(content=buffer.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={filename}.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


async def process_file(file: UploadFile, card_type: Literal["equation", "first", "second"]):

    if file.content_type == "text/csv":
        try:
            data = await file.read()
            await file.close()
            handler = CSVHandler(contents=data)
            cards = handler.list_of_dicts
        except Exception as err:
            raise HTTPException(
                status_code=422,
                detail=f"Error with file processing originated from {err}"
            )
        data = []
        for card in cards:
            print(card)
            try:
                data.append(
                    [templates_handler_factory.get_handler(card_type)(card=card)]
                )
            except Exception as err:
                print(err)
                data.append(["Error"])

        return prepare_csv_to_response(data=data, filename=f"{file.filename}_with_HTML")

    raise HTTPException(status_code=422, detail="Unprocessed file format")


@card_router.post("/equation_cards")
async def equation_card_create(file: UploadFile):
    """

        Для просмотра как будет выглядеть карточка перейди по адресу "HOST:PORT/examples/equation_card"

        Формат файла 'CSV'. Принимает файл без заголовков, но данные в установленном порядке
        "title", "header", "image_url", "rating", "description", "description_items", где:
        title - строка заголовок карточки,
        label - строка лейбл карточки,
        image_url - url адрес на котором хранится изображение,
        rating - цифра в диапазоне 1-5 включительно, будет преобразовано в звездочки,
        description - текст описание для карточки,
        description_items - текст который будет представлен в карточке как список, каждый элемент в данном тексте
        быть отделен от другого символами '; ' (точка с запятой, после которой пробел. В конце ставить не надо)
    """
    return await process_file(file=file, card_type="equation")


@card_router.post("/first")
async def first_card_type(file: UploadFile):

    return await process_file(file=file, card_type="first")


@card_router.post("/second")
async def second_card_type(file: UploadFile):

    return await process_file(file=file, card_type="second")

