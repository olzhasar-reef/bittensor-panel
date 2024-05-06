from bittensor_panel.core.bt import load_hyperparams, update_remote_hyperparam
from bittensor_panel.core.exceptions import HyperParameterUpdateFailed
from bittensor_panel.core.models import HyperParameter


def update_hyperparam(instance: HyperParameter) -> None:
    """
    Update hyperparameter in the subtensor with the new value and save changes to the database.
    """

    result = update_remote_hyperparam(instance.name, instance.value)

    if not result:
        raise HyperParameterUpdateFailed("Failed to update remote hyperparameter. Subtensor returned False.")

    instance.save(update_fields=["value"])


def refresh_hyperparams() -> None:
    """
    Load hyperparameters from the subtensor and overwrite corresponding records in the database.
    """

    hyperparam_dict = load_hyperparams()

    if not hyperparam_dict:
        return

    objs: list[HyperParameter] = []

    for name, value in hyperparam_dict.items():
        objs.append(HyperParameter(name=name, value=value))

    HyperParameter.objects.bulk_create(objs, update_conflicts=True, update_fields=["value"], unique_fields=["name"])
