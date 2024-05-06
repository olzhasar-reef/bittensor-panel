from unittest.mock import MagicMock

import pytest
from bittensor import SubnetHyperparameters
from faker import Faker
from pytest_mock import MockerFixture

from bittensor_panel.core import bt
from bittensor_panel.core.exceptions import (
    SubtensorConnectionError,
    SubtensorServerError,
)


def test_get_subtensor(mocker: MockerFixture, settings):
    mock = mocker.patch("bittensor_panel.core.bt.bittensor.subtensor", autospec=True)

    st = bt.get_subtensor()

    assert st == mock.return_value

    mock.assert_called_once_with(settings.SUBTENSOR_ADDRESS)


@pytest.mark.parametrize("exc_type", [SystemExit, RuntimeError])
def test_get_subtensor_exception(mocker: MockerFixture, exc_type):
    mocker.patch(
        "bittensor_panel.core.bt.bittensor.subtensor",
        autospec=True,
        side_effect=exc_type,
    )

    with pytest.raises(SubtensorConnectionError):
        bt.get_subtensor()


def test_get_wallet(mocker: MockerFixture, settings):
    mock = mocker.patch("bittensor_panel.core.bt.bittensor.wallet", autospec=True)

    st = bt.get_wallet()

    assert st == mock.return_value

    mock.assert_called_once_with(
        name=settings.WALLET_NAME,
        path=settings.WALLET_PATH,
    )


@pytest.fixture
def mock_subtensor(mocker: MockerFixture):
    return mocker.patch("bittensor_panel.core.bt.get_subtensor", autospec=True)


@pytest.fixture
def hyperparam_values(faker: Faker):
    return {
        "rho": faker.pyint(),
        "kappa": faker.pyint(),
        "immunity_period": faker.pyint(),
        "min_allowed_weights": faker.pyint(),
        "max_weight_limit": faker.pyint(),
        "tempo": faker.pyint(),
        "min_difficulty": faker.pyint(),
        "max_difficulty": faker.pyint(),
        "weights_version": faker.pyint(),
        "weights_rate_limit": faker.pyint(),
        "adjustment_interval": faker.pyint(),
        "activity_cutoff": faker.pyint(),
        "registration_allowed": faker.pyint(),
        "target_regs_per_interval": faker.pyint(),
        "min_burn": faker.pyint(),
        "max_burn": faker.pyint(),
        "bonds_moving_avg": faker.pyint(),
        "max_regs_per_block": faker.pyint(),
        "serving_rate_limit": faker.pyint(),
        "max_validators": faker.pyint(),
        "adjustment_alpha": faker.pyint(),
        "difficulty": faker.pyint(),
    }


@pytest.fixture
def hyperparams(hyperparam_values: dict[str, int]):
    return SubnetHyperparameters(**hyperparam_values)


def test_load_hyperparams(
    mock_subtensor: MagicMock,
    hyperparams: SubnetHyperparameters,
    hyperparam_values: dict[str, int],
):
    mock_subtensor.return_value.get_subnet_hyperparameters.return_value = hyperparams

    assert bt.load_hyperparams() == hyperparam_values


def test_load_hyperparams_empty_list(mock_subtensor: MagicMock):
    mock_subtensor.return_value.get_subnet_hyperparameters.return_value = []

    assert bt.load_hyperparams() is None


def test_load_hyperparams_exception(mock_subtensor: MagicMock):
    mock_subtensor.return_value.get_subnet_hyperparameters.side_effect = RuntimeError

    with pytest.raises(SubtensorServerError):
        bt.load_hyperparams()


@pytest.fixture
def mock_wallet(mocker: MockerFixture):
    return mocker.patch("bittensor_panel.core.bt.get_wallet", autospec=True)


@pytest.mark.parametrize("result", [True, False])
def test_update_remote_hyperparam(mock_subtensor: MagicMock, mock_wallet: MagicMock, result: bool, settings):
    mock_subtensor.return_value.set_hyperparameter.return_value = result

    name = "difficulty"
    value = "10"

    assert bt.update_remote_hyperparam(name, value) == result

    mock_subtensor.return_value.set_hyperparameter.assert_called_once_with(
        wallet=mock_wallet.return_value,
        netuid=settings.SUBNET_UID,
        parameter=name,
        value=value,
        wait_for_inclusion=False,
        wait_for_finalization=True,
        prompt=False,
    )


def test_update_remote_hyperparam_exception(mock_subtensor: MagicMock, mock_wallet: MagicMock):
    mock_subtensor.return_value.set_hyperparameter.side_effect = RuntimeError

    with pytest.raises(SubtensorServerError):
        bt.update_remote_hyperparam("difficulty", "10")
