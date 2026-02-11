"""Base MPPT driver class."""


class BaseMPPTDriver:
    """Base class for MPPT (Maximum Power Point Tracking) drivers.

    This abstract base class defines the interface that all MPPT driver
    implementations must follow.
    """

    def __init__(self, name: str) -> None:
        """Initialize the base MPPT driver.

        Args:
            name: Name of the MPPT driver instance.

        """
        self.name = name

    def get_power(self) -> float:
        """Get the current power output of the MPPT."""
        msg = "Must be implemented by subclass"
        raise NotImplementedError(msg)

    def get_voltage(self) -> float:
        """Get the current voltage output of the MPPT."""
        msg = "Must be implemented by subclass"
        raise NotImplementedError(msg)

    def get_current(self) -> float:
        """Get the current current output of the MPPT."""
        msg = "Must be implemented by subclass"
        raise NotImplementedError(msg)
