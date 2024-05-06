class BittensorAPIError(Exception):
    """Base class for all Bittensor API errors."""


class SubtensorConnectionError(BittensorAPIError):
    """Failed to connect to subtensor instance."""


class SubtensorServerError(BittensorAPIError):
    """Subtensor network returned an error."""


class HyperParameterUpdateFailed(Exception):
    """Failed to update hyperparameter in subtensor."""
