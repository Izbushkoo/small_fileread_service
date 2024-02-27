import json
from typing import Dict, Optional, Literal, List

from pydantic import BaseModel, Field, config

from wix_api import BaseObject

NODES_TYPES = Literal["TEXT", "HEADING", "PARAGRAPH"]
ALIGNMENT_TYPES = Literal["AUTO", "LEFT", "RIGHT", "CENTER", "JUSTIFY"]


class ConfigMixin(BaseModel):
    model_config = config.ConfigDict(
        extra="allow",
        populate_by_name=True
    )


class TextData(ConfigMixin):
    text: str
    decorations: Optional[List[Dict]] = Field(default_factory=list)


class TextStyle(ConfigMixin):
    text_alignment: Optional[ALIGNMENT_TYPES] = Field(alias="textAlignment")
    line_height: Optional[str] = Field(alias="lineHeight")


class HeadingData(ConfigMixin):
    level: int = Field(ge=1, le=6)
    # text_style: Optional[TextStyle] = Field(default_factory=dict, alias="textStyle")
    indentation: Optional[int] = Field(ge=1, le=6, default=0)


class ParagraphData(ConfigMixin):
    # text_style: Optional[TextStyle] = Field(default_factory=dict, alias="textStyle")
    indentation: Optional[int] = Field(ge=1, le=6, default=0)


class Node(ConfigMixin):
    type: NODES_TYPES
    id: Optional[str] = Field(default="")
    nodes: List["Node"] = Field(default_factory=list)


class RichContent(ConfigMixin):
    nodes: List[Node]
    # metadata: Optional[Dict] = Field(default_factory=dict)
    document_style: Optional[Dict] = Field(default_factory=dict, alias="documentStyle")


class DraftPost(BaseObject):
    title: str = Field(max_length=100)
    rich_content: Optional[RichContent] = Field(default_factory=dict, alias="richContent")
    memberId: str = Field(default="c2c919ed-b1f9-4038-9686-ff05bcbcdf08")

    def request_model(self) -> str:
        print(self.model_dump(by_alias=True))
        return json.dumps({
            "draftPost": self.model_dump(by_alias=True),
            "fieldSets": ["CONTENT"]
        })


