from pydantic import BaseModel

from rely.clients.models.content_tree import ContentTree


class ContentTreeList(BaseModel):
    content_tree_list: list[ContentTree]
