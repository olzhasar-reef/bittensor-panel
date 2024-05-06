from dataclasses import asdict

import bittensor
from django.conf import settings

from .exceptions import (
    SubtensorConnectionError,
    SubtensorServerError,
)


def get_subtensor() -> bittensor.subtensor:
    try:
        return bittensor.subtensor(settings.SUBTENSOR_ADDRESS)
    except (SystemExit, Exception) as e:
        raise SubtensorConnectionError(f"Failed to connect to subtensor at: {settings.SUBTENSOR_ADDRESS}") from e


def get_wallet() -> bittensor.wallet:
    return bittensor.wallet(
        name=settings.WALLET_NAME,
        path=settings.WALLET_PATH,
    )


def load_hyperparams() -> dict[str, int] | None:
    st = get_subtensor()

    try:
        hyperparams = st.get_subnet_hyperparameters(settings.SUBNET_UID)
    except Exception as e:
        raise SubtensorServerError(f"Failed to load hyperparameters from subtensor\n{e}") from e

    if not hyperparams:
        return None

    return asdict(hyperparams)


def update_remote_hyperparam(name: str, value: str) -> bool:
    st = get_subtensor()
    wallet = get_wallet()

    try:
        return st.set_hyperparameter(
            wallet=wallet,
            netuid=settings.SUBNET_UID,
            parameter=name,
            value=value,
            wait_for_inclusion=False,
            wait_for_finalization=True,
            prompt=False,
        )
    except Exception as exc:
        raise SubtensorServerError(f"Failed to update hyperparameter in subtensor\n{exc}") from exc
