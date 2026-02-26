from __future__ import annotations
from typing import Any, Iterable, Optional, Type, Union, overload


class Validator:
    """Base descriptor for attribute validation with type hints."""

    protected_name: str

    def __set_name__(self, owner: Type[object], name: str) -> None:
        self.protected_name = f"_{name}"

    @overload
    def __get__(self, instance: None, owner: Type[object]) -> Validator:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    @overload
    def __get__(self, instance: object, owner: Type[object]) -> Any:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    def __get__(
        self,
        instance: Optional[object],
        owner: Type[object]
    ) -> Union[Validator, Any]:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: Any) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    def validate(self, value: Any) -> None:
        """Abstract method for subclasses to implement."""
        raise NotImplementedError("Subclasses must implement validate().")


class Number(Validator):
    """Descriptor to validate integer ranges."""

    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value: int = min_value
        self.max_value: int = max_value

    def validate(self, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator):
    """Descriptor to validate value is within a specific set of options."""

    def __init__(self, options: Iterable[str]) -> None:
        self.options: Iterable[str] = options

    def validate(self, value: Any) -> None:
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {self.options}."
            )


class BurgerRecipe:
    """Class representing a burger recipe with type-hinted attributes."""

    # Descriptor declarations as class attributes
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

    def __init__(
        self,
        buns: int,
        cheese: int,
        tomatoes: int,
        cutlets: int,
        eggs: int,
        sauce: str
    ) -> None:
        self.buns: int = buns
        self.cheese: int = cheese
        self.tomatoes: int = tomatoes
        self.cutlets: int = cutlets
        self.eggs: int = eggs
        self.sauce: str = sauce
