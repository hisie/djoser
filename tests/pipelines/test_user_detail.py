import pytest

from django.contrib.auth import authenticate, get_user_model

from djoser import exceptions, pipelines, signals
from tests.common import catch_signal, mock

User = get_user_model()


@pytest.mark.django_db(transaction=False)
def test_valid_perform(test_user):
    request = mock.MagicMock()
    request.user = test_user
    result = pipelines.user_detail.perform(request, {})

    assert result['user'] == test_user


@pytest.mark.django_db(transaction=False)
def test_valid_serialize_instance(test_user):
    context = {'user': test_user}
    result = pipelines.user_detail.serialize_instance(None, context)
    username = getattr(test_user, User.USERNAME_FIELD)

    assert 'response_data' in result
    assert result['response_data'] == {
        'id': 1,
        'email': test_user.email,
        User.USERNAME_FIELD: username,
    }


@pytest.mark.django_db(transaction=False)
def test_valid_pipeline(test_user):
    request = mock.MagicMock()
    request.user = test_user
    username = getattr(test_user, User.USERNAME_FIELD)

    pipeline = pipelines.user_detail.Pipeline(request)
    result = pipeline.run()

    assert 'response_data' in result
    assert result['response_data'] == {
        'id': 1,
        'email': test_user.email,
        User.USERNAME_FIELD: username,
    }
