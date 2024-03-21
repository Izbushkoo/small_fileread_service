from typing import List, Optional, Dict, Callable
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field, AnyUrl


class Card(BaseModel):
    title: str
    label: str
    image_url: AnyUrl
    rating: int = Field(le=5, ge=1)
    description: Optional[str] = None
    description_items: Optional[List[str]]


file_loader = FileSystemLoader("jinja_process/templates")
examples_loader = FileSystemLoader("jinja_process/example_templates")
env = Environment(loader=file_loader)
examples_environment = Environment(loader=examples_loader)


class TemplatesFactory:

    def __init__(self):
        self.handlers = {}

    def register_handler(self, name: str, handler: Callable):
        self.handlers[name] = handler

    def get_handler(self, name: str):
        handler = self.handlers.get(name, None)
        if not handler:
            raise KeyError(f"Handler with name '{name}' was not registered")
        return handler


def construct_equation_html(card: Dict):
    return env.get_template("equation_template.htm").render(card=card)


def example_equation():
    return examples_environment.get_template("equation_example.html").render()


def construct_first_card_type(card: Dict):
    return env.get_template("card_type_1.htm").render(card=card)


def example_first_type():
    return examples_environment.get_template("example_type_1.html").render()


def construct_second_card_type(card: Dict):
    return env.get_template("card_type_2.htm").render(card=card)


def example_second_type():
    return examples_environment.get_template("example_type_2.html").render()


templates_handler_factory = TemplatesFactory()
templates_handler_factory.register_handler("equation", construct_equation_html)
templates_handler_factory.register_handler("first", construct_first_card_type)
templates_handler_factory.register_handler("second", construct_second_card_type)

# templates_handler_factory.register_handler("example_equation", example_equation)
# templates_handler_factory.register_handler("example_first", example_first_type)
# templates_handler_factory.register_handler("example_second", example_second_type)



