from unittest.mock import MagicMock

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from bittensor_panel.core.exceptions import HyperParameterUpdateFailed
from bittensor_panel.core.models import HyperParameter
from bittensor_panel.core.services import (
    refresh_hyperparams,
    update_hyperparam,
)

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def hyperparam():
    return HyperParameter.objects.create(
        name="test",
        value="123",
    )


@pytest.fixture
def mock_update_remote_hyperparam(mocker: MockerFixture):
    return mocker.patch("bittensor_panel.core.services.update_remote_hyperparam")


def test_update_hyperparam(
    hyperparam: HyperParameter,
    mock_update_remote_hyperparam: MagicMock,
    django_assert_num_queries,
):
    mock_update_remote_hyperparam.return_value = True

    new_value = "999"

    hyperparam.value = new_value

    with django_assert_num_queries(1):
        update_hyperparam(hyperparam)

    mock_update_remote_hyperparam.assert_called_once_with(hyperparam.name, new_value)

    hyperparam.refresh_from_db()
    assert hyperparam.value == new_value


def test_update_hyperparam_remote_returns_false(
    hyperparam: HyperParameter,
    mock_update_remote_hyperparam: MagicMock,
    django_assert_num_queries,
):
    mock_update_remote_hyperparam.return_value = False

    hyperparam.value = "999"

    with django_assert_num_queries(0):
        with pytest.raises(HyperParameterUpdateFailed):
            update_hyperparam(hyperparam)


def test_update_hyperparam_remote_exception(
    hyperparam: HyperParameter,
    mock_update_remote_hyperparam: MagicMock,
    django_assert_num_queries,
):
    mock_update_remote_hyperparam.side_effect = RuntimeError

    hyperparam.value = "999"

    with django_assert_num_queries(0):
        with pytest.raises(RuntimeError):
            update_hyperparam(hyperparam)


@pytest.fixture
def hyperparam_dict(faker: Faker):
    return {faker.word(): str(faker.pyint()) for _ in range(10)}


@pytest.fixture
def mock_load_hyperparams(mocker: MockerFixture, hyperparam_dict: dict[str, int]):
    return mocker.patch("bittensor_panel.core.services.load_hyperparams", return_value=hyperparam_dict)


def test_refresh_hyperparams(
    hyperparam_dict: dict[str, int],
    mock_load_hyperparams: MagicMock,
    django_assert_num_queries,
):
    assert not HyperParameter.objects.exists()

    with django_assert_num_queries(1):
        refresh_hyperparams()

    assert HyperParameter.objects.count() == len(hyperparam_dict)

    for name, value in HyperParameter.objects.values_list("name", "value"):
        assert hyperparam_dict[name] == value


def test_refresh_hyperparams_existing_records(
    hyperparam_dict: dict[str, int],
    mock_load_hyperparams: MagicMock,
    django_assert_num_queries,
):
    for name in hyperparam_dict:
        HyperParameter.objects.create(name=name, value=0)

    with django_assert_num_queries(1):
        refresh_hyperparams()

    assert HyperParameter.objects.count() == len(hyperparam_dict)

    for name, value in HyperParameter.objects.values_list("name", "value"):
        assert hyperparam_dict[name] == value


def test_refresh_hyperparams_exception(
    mock_load_hyperparams: MagicMock,
    django_assert_num_queries,
):
    mock_load_hyperparams.side_effect = RuntimeError

    with django_assert_num_queries(0):
        with pytest.raises(RuntimeError):
            refresh_hyperparams()

    assert not HyperParameter.objects.exists()
