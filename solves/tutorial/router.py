from deepdiff import DeepDiff
from django.urls import URLPattern, URLResolver

from utils import SolveDecorator, dec


@SolveDecorator
def solve1(urlpatterns):
    want_resolve = {
        'user-list': 'users/',
        'user-detail': 'users/1/',
    }

    remain = want_resolve.copy()

    for urlpattern in urlpatterns:
        if isinstance(urlpattern, URLPattern):
            if remain.get(urlpattern.name, None):
                if urlpattern.pattern.match(remain.get(urlpattern.name)):
                    del remain[urlpattern.name]

    for key, value in remain.items():
        assert False, f'{value} URL 이 동작하지 않습니다.'


@SolveDecorator
def solve2(answer1, answer2, answer3, answer4):
    result1 = [
        'accounts/', 'accounts/<int:pk>/'
    ]
    diff = DeepDiff(answer1, result1, ignore_order=True)
    assert not diff.tree, 'answer1 번이 틀렸습니다'

    result2 = [
        'user-list', 'user-detail',
    ]
    diff = DeepDiff(answer2, result2, ignore_order=True)
    assert not diff.tree, 'answer2 번이 틀렸습니다'

    result3 = [
        'people/', 'people/<int:pk>/',
    ]
    diff = DeepDiff(answer3, result3, ignore_order=True)
    assert not diff.tree, 'answer3 번이 틀렸습니다'

    result4 = [
        'person-list', 'person-detail',
    ]
    diff = DeepDiff(answer4, result4, ignore_order=True)
    assert not diff.tree, 'answer4 번이 틀렸습니다'


@SolveDecorator
def solve3(urlpatterns1, urlpatterns2):
    result = {
        '+=': False,
        'include': False,
    }

    for urlpattern in urlpatterns1:
        if isinstance(urlpattern, URLPattern):
            result['+='] = True

        if isinstance(urlpattern, URLResolver):
            result['include'] = True

    for urlpattern in urlpatterns2:
        if isinstance(urlpattern, URLPattern):
            result['+='] = True

        if isinstance(urlpattern, URLResolver):
            result['include'] = True

    for key, value in result.items():
        if not value:
            assert False, f'`{key}` 를 사용하여 URL 을 연결해주세요.'


@SolveDecorator
def solve4(answer1, answer2):
    result1 = dec(b'InVzZXJzLzxpbnQ6cGs+L3NldF9hZG1pbiI=')
    result2 = dec(b'InVzZXItc2V0LWFkbWluIg==')
    assert answer1 == result1, 'answer1 번이 틀렸습니다.'
    assert answer2 == result2, 'answer2 번이 틀렸습니다.'


@SolveDecorator
def solve5(urlpatterns):
    want_resolve = [
        ['user-set-admin', False, 'reverse name'],
        ['users/1/change-admin/', False, 'URL'],
    ]

    for urlpattern in urlpatterns:
        if urlpattern.name == want_resolve[0][0]:
            want_resolve[0][1] = True

        if urlpattern.pattern.match(want_resolve[1][0]):
            want_resolve[1][1] = True

    for key, value, question in want_resolve:
        assert value, f'{question}: {key} 가 설정되지 않았습니다.'
