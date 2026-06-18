"""
Design & Analysis

Input/Output (I/O):
- Input: name (str), bonus_atk (number), bonus_speed (number)
- Action: binary operator + between two Companion objects
- Output: new Companion object (on successful breeding), console messages when skills are used,
  TypeError raised for invalid operations (instantiating abstract base or cross-type breeding)

Architecture & Logic:
- Use `abc` to define `Companion` with @abstractmethod `unleash_skill` to prevent direct instantiation.
- `Companion` manages `name` and `level` (default=1) and provides a template for __add__.
- `Pet` and `Mount` inherit `Companion`. They accept **kwargs and call super().__init__(**kwargs)
  so that `Dragon(Pet, Mount)` can route parameters through MRO using super().
- `Dragon` inherits from both `Pet` and `Mount` and uses cooperative __init__ to ensure both
  bonus_atk and bonus_speed are initialized.
- __add__ is implemented to only allow combining two objects of the same exact type
  (type(self) == type(other)). On mismatch, raise TypeError("Chỉ có thể lai tạo 2 sinh vật cùng loài!").

"""

from abc import ABC, abstractmethod
from typing import Any, List


class Companion(ABC):
    """Abstract base for all companions.

    Attributes:
        name (str)
        level (int)
    """

    def __init__(self, name: str, level: int = 1, **kwargs: Any):
        self.name = name
        self.level = int(level)

    @abstractmethod
    def unleash_skill(self) -> None:
        """Each companion must implement its unique skill effect."""

    def __add__(self, other: Any):
        # General guard: other must be a Companion and same concrete type
        if not isinstance(other, Companion):
            raise TypeError("Chỉ có thể lai tạo 2 sinh vật cùng loài!")
        if type(self) is not type(other):
            raise TypeError("Chỉ có thể lai tạo 2 sinh vật cùng loài!")
        # Delegation to concrete implementations
        raise NotImplementedError("Subclasses must implement their own __add__")


class Pet(Companion):
    def __init__(self, name: str, level: int = 1, bonus_atk: int = 0, **kwargs: Any):
        super().__init__(name=name, level=level, **kwargs)
        self.bonus_atk = int(bonus_atk)

    def unleash_skill(self) -> None:
        print(f"{self.name} gầm gừ: Tấn công kẻ thù, gây {self.bonus_atk} sát thương!")

    def __add__(self, other: Any):
        if not isinstance(other, Companion) or type(self) is not type(other):
            raise TypeError("Chỉ có thể lai tạo 2 sinh vật cùng loài!")
        new_name = f"{self.name} {other.name}"
        new_level = self.level + 1
        new_atk = self.bonus_atk + other.bonus_atk
        return Pet(new_name, level=new_level, bonus_atk=new_atk)

    def display(self) -> str:
        return f"[Pet] {self.name} | Cấp: {self.level} | Atk: +{self.bonus_atk}"


class Mount(Companion):
    def __init__(self, name: str, level: int = 1, bonus_speed: int = 0, **kwargs: Any):
        super().__init__(name=name, level=level, **kwargs)
        self.bonus_speed = int(bonus_speed)

    def unleash_skill(self) -> None:
        print(f"{self.name} hí vang: Tăng tốc độ di chuyển thêm {self.bonus_speed} điểm!")

    def __add__(self, other: Any):
        if not isinstance(other, Companion) or type(self) is not type(other):
            raise TypeError("Chỉ có thể lai tạo 2 sinh vật cùng loài!")
        new_name = f"{self.name} {other.name}"
        new_level = self.level + 1
        new_speed = self.bonus_speed + other.bonus_speed
        return Mount(new_name, level=new_level, bonus_speed=new_speed)

    def display(self) -> str:
        return f"[Mount] {self.name} | Cấp: {self.level} | Speed: +{self.bonus_speed}"


class Dragon(Pet, Mount):
    def __init__(self, name: str, level: int = 1, bonus_atk: int = 0, bonus_speed: int = 0, **kwargs: Any):
        # Use cooperative multiple inheritance: pass all params along
        super().__init__(name=name, level=level, bonus_atk=bonus_atk, bonus_speed=bonus_speed, **kwargs)

    def unleash_skill(self) -> None:
        print(f"{self.name} thị uy:")
        # Call Pet behavior and Mount behavior explicitly to ensure both happen
        Pet.unleash_skill(self)
        Mount.unleash_skill(self)

    def __add__(self, other: Any):
        if not isinstance(other, Companion) or type(self) is not type(other):
            raise TypeError("Chỉ có thể lai tạo 2 sinh vật cùng loài!")
        new_name = f"{self.name} {other.name}"
        new_level = self.level + 1
        new_atk = self.bonus_atk + other.bonus_atk
        new_speed = self.bonus_speed + other.bonus_speed
        return Dragon(new_name, level=new_level, bonus_atk=new_atk, bonus_speed=new_speed)

    def display(self) -> str:
        return f"[Dragon] {self.name} | Cấp: {self.level} | Atk: +{self.bonus_atk} | Speed: +{self.bonus_speed}"


def main():
    print("--- Kiểm thử hệ thống Companion ---")

    # 1) Thử khởi tạo Companion trực tiếp -> phải lỗi
    try:
        c = Companion("Lỗi thử")
    except TypeError as e:
        print("Không thể khởi tạo Companion trực tiếp:", e)

    # 2) Tạo pets
    p1 = Pet("Sói Trắng", bonus_atk=50)
    p2 = Pet("Sói Đen", bonus_atk=60)
    print(p1.display())
    print(p2.display())

    # 3) Lai tạo p1 + p2
    p3 = p1 + p2
    print("\n>> Lai tạo thành công:")
    print(p3.display())

    # 4) Test bẫy 2: Pet + Mount and Pet + number
    m1 = Mount("Hắc Mã", bonus_speed=20)
    try:
        bad = p1 + m1
    except TypeError as e:
        print("Bẫy lai tạo khác loài bị chặn:", e)

    try:
        bad2 = p1 + 10
    except TypeError as e:
        print("Bẫy lai tạo với số bị chặn:", e)

    # 5) Tạo Dragon và kiểm tra cả 2 chỉ số
    d1 = Dragon("Rồng Lửa", bonus_atk=500, bonus_speed=200)
    print("\n", d1.display())

    # 6) Đa hình: unleash_skill for each
    equipped: List[Companion] = [p3, m1, d1]
    print("\n--- Xuất chiến (Polymorphism) ---")
    for comp in equipped:
        comp.unleash_skill()


if __name__ == "__main__":
    main()
