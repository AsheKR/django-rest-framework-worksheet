import base64
import json
import typing
from collections import defaultdict

from django.db.transaction import Atomic, get_connection
from rest_framework.routers import BaseRouter

__all__ = (
    'enc',
    'dec',
    'AtomicRollback',
    'get_actions_from_router',
)


def enc(data: typing.Any) -> bytes:
    json_data = json.dumps(data)
    return base64.b64encode(json_data.encode('utf-8'))


def dec(data: bytes) -> typing.Any:
    json_data = base64.b64decode(data).decode('utf-8')
    return json.loads(json_data)


def get_actions_from_router(router: BaseRouter) -> (typing.Dict[str, typing.List[str]], typing.Dict[str, typing.List[str]], ):
    result_group_by_method = defaultdict(list)
    result_group_by_action = defaultdict(list)
    for url in router.urls:
        for key, value in url.callback.actions.items():
            result_group_by_method[key].append(value)
            result_group_by_action[value].append(key)

    return result_group_by_method, result_group_by_action


class AtomicRollback(Atomic):
    def __init__(self, using=None, savepoint=None):
        super().__init__(using, savepoint)

    def __exit__(self, *args, **kwargs):
        connection = get_connection(self.using)
        connection.needs_rollback = True
        super().__exit__(*args, **kwargs)
