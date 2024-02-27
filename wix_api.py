import json
import os
from enum import Enum
from typing import Dict, List, Tuple

import httpx
from pydantic.config import ConfigDict
from pydantic import BaseModel, Field

from config import settings


class Route(BaseModel):
    endpoint: str
    method: str
    format_variables: Tuple[str] = Field(default=None)


class BaseRoute(Enum):
    route: Route


class CatalogRoute(BaseRoute):

    get_product = Route(endpoint="/stores-reader/v1/products/{id}", method="get", format_variables=("id", ))
    create_product = Route(endpoint="/stores/v1/products", method="post")
    update_product = Route(endpoint="/stores/v1/products/{id}", method="patch", format_variables=("id", ))
    delete_product = Route(endpoint="/stores/v1/products/{id}", method="delete", format_variables=("id", ))
    add_product_media = Route(endpoint="/stores/v1/products/{id}/media", method="post", format_variables=("id", ))
    remove_product_media = Route(endpoint="/stores/v1/products/{id}/media/delete", method="post",
                                 format_variables=("id", ))


class WixBlogRoute(BaseRoute):
    create_draft_post = Route(endpoint="/blog/v3/draft-posts", method="post")


class AbsentCredentials(ValueError):
    """Credentials does not provided"""


class BaseApiException(Exception):
    pass


class InvalidRequestBody(BaseApiException):
    pass


class APIError(BaseApiException):
    pass


class APIResponseError(BaseApiException):
    pass


class EmptyUpdateProductValues(BaseApiException):
    pass


class ProductUpdateError(BaseApiException):
    pass


class BaseObject(BaseModel):
    """Base Object to inherit"""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        populate_by_name=True,
        extra="allow"
    )

    def request_model(self) -> Dict:
        """Rewrite. Used for getting model to create wix api request."""


class BaseCredentials:

    @classmethod
    def _validate_credentials_as_headers(cls, **kwargs) -> Dict[str, str]:

        account_id = os.getenv("WIX_ACCOUNT_ID") or kwargs.get("account_id")
        if not account_id:
            raise AbsentCredentials("""'WIX_ACCOUNT_ID' environment or 'account_id' kwarg must be provided""")
        site_id = os.getenv("WIX_SITE_ID") or kwargs.get("site_id")
        if not site_id:
            raise AbsentCredentials("""'WIX_SITE_ID' environment or 'site_id' kwarg must be provided""")
        api_token = os.getenv("WIX_API_KEY") or kwargs.get("api_token")
        if not api_token:
            raise AbsentCredentials("""'WIX_API_KEY' environment or 'api_token' kwarg must be provided""")
        return {
            "Authorization": api_token,
            "wix-account-id": account_id,
            "wix-site-id": site_id
        }


class BaseClient(BaseCredentials):

    base_url = "https://www.wixapis.com"

    def __init__(self, **kwargs):
        self.headers = BaseCredentials._validate_credentials_as_headers(**kwargs)


class AsyncClient(BaseClient):

    async def make_request(self, body: BaseObject, route: BaseRoute, **kwargs):
        """'path_params' - Dict with key-value where key is a path parameter name and value is format value.
        Crucial only when Route path has format variables.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as session:
            if route.value.format_variables:
                try:
                    path_params = kwargs["path_params"]
                    prepare_format_dict = {key: path_params.get(key) for key in route.value.format_variables}
                except (ValueError, AttributeError, KeyError):
                    raise InvalidRequestBody(
                        """Was passed invalid "path_params" keyword argument with path route variables"""
                    )
                prepared_path = route.value.endpoint.format(**prepare_format_dict)
            else:
                prepared_path = route.value.endpoint

            response = await session.request(
                method=route.value.method,
                url=prepared_path,
                data=body.request_model()
            )
            if response.status_code == 200:
                return response
            raise APIResponseError(f"An error occurred. Origin status code {response.status_code}\n"
                                   f"Details: {str(response.content)}")
