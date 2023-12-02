from dataclasses import dataclass


@dataclass
class TgSupplier:
    def __post_init__(self) -> None:
        ...
