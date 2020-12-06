from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework.routers import SimpleRouter
from rest_framework.test import APIRequestFactory
from rest_framework.utils.serializer_helpers import ReturnList

from utils import dec, get_actions_from_router, SolveDecorator


User = get_user_model()


@SolveDecorator
def solve1(view):
    allow_methods = dec(
        b'eyJwb3N0IjogWyJjcmVhdGUiXSwgInBhdGNoIjogWyJwYXJ0aWFsX3VwZGF0ZSJdLCAiZGVsZXRlIjogWyJkZXN0cm95Il19'
    )
    router = SimpleRouter()
    router.register('users', view)

    group_by_methods, _ = get_actions_from_router(router)
    result_methods = allow_methods.copy()

    for method in group_by_methods:
        if method in result_methods:
            del result_methods[method]

    assert not result_methods, f'{", ".join([value for key, values in result_methods.items() for value in values])} 이(가) 구현되지 않았습니다.'


@SolveDecorator
def solve2(view):
    action_name = dec(b'InNldF9zdGFmZiI=')
    allow_method = dec(b'InBvc3Qi')

    router = SimpleRouter()
    router.register('users', view)

    _, group_by_actions = get_actions_from_router(router)

    assert group_by_actions.get(action_name, None), 'set_staff action 이 구현되지 않았습니다.'
    assert allow_method in group_by_actions.get(action_name,
                                                []), f'set_staff action 는 POST Method 를 허용해야합니다. 현재 set_staff action 은 {", ".join(group_by_actions.get(action_name, []))} 을 허용중입니다.'

    factory = APIRequestFactory()
    view = view.as_view(actions={allow_method: action_name})
    user = baker.make(User, is_staff=False)
    response = view(factory.post(''), pk=user.pk)

    assert response.status_code == 200, f'{allow_method} API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    user.refresh_from_db()
    assert user.is_staff, f'{allow_method} API 호출 결과 유저의 is_staff 속성이 True 로 설정되지 않았습니다.'


@SolveDecorator
def solve3(view):
    action_name = dec(b'ImVtYWlsIg==')
    allow_method = dec(b'WyJnZXQiLCAiZGVsZXRlIl0=')

    router = SimpleRouter()
    router.register('users', view)

    group_by_methods, group_by_actions = get_actions_from_router(router)

    assert group_by_actions.get(action_name, None), 'email action 이 구현되지 않았습니다.'
    assert allow_method == group_by_actions.get(action_name,
                                                []), f'email action 은 GET, DELETE Method 를 허용해야합니다. 현재 email action 은 {", ".join(group_by_actions.get(action_name, []))} 을 허용중입니다.'

    factory = APIRequestFactory()

    view = view.as_view(actions={'get': action_name})
    user = baker.make(User, email='admin@ashe.kr')
    response = view(factory.get(''), pk=user.pk)

    assert response.status_code == 200, f'get API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    assert response.data == 'admin@ashe.kr', f'get API 호출 결과는 {"admin@ashe.kr"} 이 되어야 합니다: 현재: {response.data}'

    view = view.as_view(actions={'delete': action_name})
    response = view(factory.delete(''), pk=user.pk)

    user.refresh_from_db()
    assert response.status_code == 204, f'delete API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    assert not user.email, 'delete API 호출 결과 유저의 email 속성이 지워지지 않았습니다.'


@SolveDecorator
def solve4(view):
    router = SimpleRouter()
    router.register('users', view)

    group_by_methods, group_by_actions = get_actions_from_router(router)

    action_name = 'email'
    allow_method = ['get']
    assert group_by_actions.get(action_name, None), 'email action 이 구현되지 않았습니다.'
    assert allow_method == group_by_actions.get(action_name,
                                                []), f'email action 은 GET Method 를 허용해야합니다. 현재 email action 은 {", ".join(group_by_actions.get(action_name, []))} 을 허용중입니다.'

    factory = APIRequestFactory()
    user = baker.make(User, email='admin@ashe.kr')

    view = view.as_view(actions={'get': 'email'})
    response = view(factory.get(''), pk=user.pk)

    assert response.status_code == 200, f'get API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    assert response.data == 'admin@ashe.kr', f'get API 호출 결과는 {"admin@ashe.kr"} 이 되어야 합니다: 현재: {response.data}'

    action_name = 'delete_email'
    allow_method = ['delete']
    assert group_by_actions.get(action_name, None), 'delete_email action 이 구현되지 않았습니다.'
    assert allow_method == group_by_actions.get(action_name,
                                                []), f'delete_email action 은 DELETE Method 를 허용해야합니다. 현재 email action 은 {", ".join(group_by_actions.get(action_name, []))} 을 허용중입니다.'

    view = view.as_view(actions={'delete': 'delete_email'})
    response = view(factory.delete(''), pk=user.pk)

    user.refresh_from_db()
    assert response.status_code == 204, f'delete API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    assert not user.email, 'delete API 호출 결과 유저의 email 속성이 지워지지 않았습니다.'


@SolveDecorator
def solve5(view):
    allow_methods = {'get': ['list', 'retrieve'], 'delete': ['destroy']}

    router = SimpleRouter()
    router.register('users', view)

    group_by_methods, _ = get_actions_from_router(router)
    result_methods = allow_methods.copy()

    for method in group_by_methods:
        if method in result_methods:
            del result_methods[method]

    assert not result_methods, f'{", ".join([value for key, values in result_methods.items() for value in values])} 이(가) 구현되지 않았습니다.'

    # Method 체크

    factory = APIRequestFactory()
    user = baker.make(User, email='admin@ashe.kr')

    # List
    view = view.as_view(actions={'get': 'list'})
    response = view(factory.get(''))

    assert response.status_code == 200, f'list API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    assert type(response.data) == ReturnList, f'list API 의 호출결과가 list 타입이 아닙니다: 현재 {type(response.data)}'
    assert {data.get('email'): data for data in response.data}.get(
        'admin@ashe.kr'), f'list API 의 호출 결과에서 테스트 데이터를 찾을 수 없습니다.'

    # Retrieve
    view = view.as_view(actions={'get': 'retrieve'})
    response = view(factory.get(''), pk=user.pk)

    assert response.status_code == 200, f'retrieve API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'

    # Delete
    view = view.as_view(actions={'delete': 'destroy'})
    response = view(factory.delete(''), pk=user.pk)

    assert response.status_code == 204, f'destroy API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    assert not User.objects.filter(pk=user.pk).first(), f'destroy API 호출 결과로 User 가 삭제되지 않았습니다.'


@SolveDecorator
def solve6(view, serializer):
    allow_methods = dec(
        b'eyJnZXQiOiBbImxpc3QiLCAicmV0cmlldmUiXSwgInBvc3QiOiBbImNyZWF0ZSJdLCAicHV0IjogWyJ1cGRhdGUiXSwgInBhdGNoIjogWyJwYXJ0aWFsX3VwZGF0ZSJdLCAiZGVsZXRlIjogWyJkZXN0cm95Il19')

    router = SimpleRouter()
    router.register('users', view)

    group_by_methods, _ = get_actions_from_router(router)
    result_methods = allow_methods.copy()

    for method in group_by_methods:
        if method in result_methods:
            del result_methods[method]

    assert not result_methods, f'{", ".join([value for key, values in result_methods.items() for value in values])} 이(가) 구현되지 않았습니다.'

    # Method 체크

    factory = APIRequestFactory()
    user = baker.make(User, email='admin@ashe.kr')

    # List
    view = view.as_view(actions={'get': 'list'})
    response = view(factory.get(''))

    assert response.status_code == 200, f'list API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    assert type(response.data) == ReturnList, f'list API 의 호출결과가 list 타입이 아닙니다: 현재 {type(response.data)}'
    assert {data.get('email'): data for data in response.data}.get(
        'admin@ashe.kr'), f'list API 의 호출 결과에서 테스트 데이터를 찾을 수 없습니다.'

    # Retrieve
    view = view.as_view(actions={'get': 'retrieve'})
    response = view(factory.get(''), pk=user.pk)

    assert response.status_code == 200, f'retrieve API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'

    # Create
    view = view.as_view(actions={'post': 'create'})
    request_data = serializer(baker.prepare(User, email='second@ashe.kr')).data
    response = view(factory.post('', request_data, format='json'))

    assert response.status_code == 201, f'create API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    assert User.objects.filter(email='second@ashe.kr').first(), 'create API 호출 결과로 User 가 생성되지 않았습니다.'

    # Update
    view = view.as_view(actions={'put': 'update'})
    user.refresh_from_db()
    request_data = serializer(user).data
    request_data['email'] = 'third@ashe.kr'
    response = view(factory.put('', request_data, format='json'), pk=user.pk)

    assert response.status_code == 200, f'update API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    user.refresh_from_db()
    assert user.email == 'third@ashe.kr', 'update API 호출 결과로 email 이 업데이트 되지 않았습니다.'

    # Partial-Update
    view = view.as_view(actions={'patch': 'partial_update'})
    user.refresh_from_db()
    request_data = serializer(user).data
    request_data['email'] = 'forth@ashe.kr'
    response = view(factory.patch('', request_data, format='json'), pk=user.pk)

    assert response.status_code == 200, f'partial_update API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    user.refresh_from_db()
    assert user.email == 'forth@ashe.kr', 'partial_update API 호출 결과로 email 이 업데이트 되지 않았습니다.'

    # Delete
    view = view.as_view(actions={'delete': 'destroy'})
    response = view(factory.delete(''), pk=user.pk)

    assert response.status_code == 204, f'destroy API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    assert not User.objects.filter(pk=user.pk).first(), f'destroy API 호출 결과로 User 가 삭제되지 않았습니다.'


@SolveDecorator
def solve7(view, serializer):
    allow_methods = {'get': ['list', 'retrieve'], 'post': ['create']}

    router = SimpleRouter()
    router.register('users', view)

    group_by_methods, _ = get_actions_from_router(router)
    result_methods = allow_methods.copy()

    for method in group_by_methods:
        if method in result_methods:
            del result_methods[method]

    assert not result_methods, f'{", ".join([value for key, values in result_methods.items() for value in values])} 이(가) 구현되지 않았습니다.'

    # Method 체크

    factory = APIRequestFactory()
    user = baker.make(User, email='admin@ashe.kr')

    # List
    view = view.as_view(actions={'get': 'list'})
    response = view(factory.get(''))

    assert response.status_code == 200, f'list API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    assert type(response.data) == ReturnList, f'list API 의 호출결과가 list 타입이 아닙니다: 현재 {type(response.data)}'
    assert {data.get('email'): data for data in response.data}.get(
        'admin@ashe.kr'), f'list API 의 호출 결과에서 테스트 데이터를 찾을 수 없습니다.'

    # Create
    view = view.as_view(actions={'post': 'create'})
    request_data = serializer(baker.prepare(User, email='second@ashe.kr')).data
    response = view(factory.post('', request_data, format='json'))

    assert response.status_code == 201, f'create API 호출 결과의 status_code 가 일치하지 않습니다: 현재: {response.status_code}'
    assert User.objects.filter(email='second@ashe.kr').first(), 'create API 호출 결과로 User 가 생성되지 않았습니다.'
