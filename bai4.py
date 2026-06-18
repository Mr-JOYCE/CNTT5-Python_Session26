# System Design & Analysis
#
# 1) Abstract Base Class:
#    - `Equipment` is the abstract base that defines the contract for all equipment
#      types. By marking `calculate_total_damage()` as `@abstractmethod`, we prevent
#      instantiation of incomplete equipment and force future developers to implement
#      the damage formula for new equipment types (e.g., Bow). This enforces "fail fast"—
#      missing implementations are detected at class-instantiation time.
#
# 2) Multiple Inheritance & MRO (MagicSword):
#    - Declaration: `class MagicSword(Weapon, MagicMixin)`
#    - MRO for `MagicSword`: [MagicSword, Weapon, MagicMixin, Equipment, ABC, object]
#    - `MagicSword.__init__` should call `Weapon.__init__` first to initialize
#      equipment attributes, then call `MagicMixin.__init__` to set `magic_power`.
#      That ordering ensures Weapon/Equipment attributes exist when MagicMixin
#      methods run. Example implementation uses explicit parent calls rather than
#      relying on cooperative super() because `MagicMixin` is a simple mixin.
#
# 3) Polymorphism:
#    - The inventory loop calls `item.calculate_total_damage()` for every item.
#      Each concrete subclass implements its own damage formula. The loop does
#      not need to check the item's type — this is polymorphism (and duck typing)
#      which makes it easy to add new weapon types without changing inventory code.
#
# 4) Operator Overloading (pseudocode for Weapon.__add__):
#    def __add__(self, other):
#        if not isinstance(other, Weapon):
#            print("Chỉ có thể dung hợp/so sánh giữa các trang bị!")
#            return None
#        new_name = f"Fusion({self.name} + {other.name})"
#        new_base = self.base_damage + other.base_damage
#        new_upgrade = self.upgrade_level + other.upgrade_level
#        return Weapon("FUSION", new_name, new_base, new_upgrade)
#    - The method returns a `Weapon` instance (or `None` on invalid input).

from abc import ABC, abstractmethod
from typing import List, Optional


class Equipment(ABC):
	"""Abstract base class for equipment items.

	Subclasses must implement calculate_total_damage().
	"""

	@abstractmethod
	def calculate_total_damage(self) -> float:
		pass


class Weapon(Equipment):
	"""Physical weapon.

	Attributes:
		name (str)
		base_damage (int)
		upgrade_level (int)
	"""

	def __init__(self, name: str, base_damage: int, upgrade_level: int = 0):
		self.name = name.title()
		if not isinstance(base_damage, (int, float)) or base_damage <= 0:
			raise ValueError("Base damage must be a positive number")
		if not isinstance(upgrade_level, int) or upgrade_level <= 0:
			raise ValueError("Upgrade level must be a positive integer")
		self.base_damage = int(base_damage)
		self.upgrade_level = int(upgrade_level)

	def calculate_total_damage(self) -> float:
		return float(self.base_damage + (self.upgrade_level * 10))

	def __gt__(self, other: 'Equipment') -> bool:
		if not isinstance(other, Equipment):
			print("Chỉ có thể dung hợp/so sánh giữa các trang bị!")
			return False
		return self.calculate_total_damage() > other.calculate_total_damage()

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Equipment):
			return False
		return self.calculate_total_damage() == other.calculate_total_damage()

	def __add__(self, other: 'Equipment') -> Optional['Weapon']:
		# Fusion: only between Weapon-like items
		if not isinstance(other, Weapon):
			print("Chỉ có thể dung hợp/so sánh giữa các trang bị!")
			return None
		new_name = f"Fusion({self.name} + {other.name})"
		new_base = self.base_damage + other.base_damage
		new_upgrade = self.upgrade_level + other.upgrade_level
		return Weapon(new_name, new_base, new_upgrade)

	def display(self) -> str:
		return f"{self.name} | Loại: Weapon | Cấp: {self.upgrade_level} | Sát thương: {int(self.calculate_total_damage())}"


class MagicMixin:
	"""Mixin providing magic power and a visual cast method."""

	def __init__(self, magic_power: int):
		if not isinstance(magic_power, (int, float)) or magic_power <= 0:
			raise ValueError("Magic power must be a positive number")
		self.magic_power = int(magic_power)

	def cast_glow(self) -> None:
		print(f"-> Vũ khí phát sáng với sức mạnh phép thuật: {self.magic_power}")


class MagicSword(Weapon, MagicMixin):
	"""A magical sword: physical weapon + magical power."""

	def __init__(self, name: str, base_damage: int, upgrade_level: int, magic_power: int):
		# Initialize Weapon part
		Weapon.__init__(self, name, base_damage, upgrade_level)
		# Initialize MagicMixin explicitly to ensure magic_power exists
		MagicMixin.__init__(self, magic_power)

	def calculate_total_damage(self) -> float:
		phys = self.base_damage + (self.upgrade_level * 10)
		return float(phys + self.magic_power)

	def display(self) -> str:
		return f"{self.name} | Loại: MagicSword | Cấp: {self.upgrade_level} | Sát thương gốc: {self.base_damage} | Sức mạnh phép thuật: {self.magic_power} | Sát thương tổng: {int(self.calculate_total_damage())}"


def print_inventory(inv: List[Equipment]) -> None:
	print("\n--- KHO VŨ KHÍ CỦA NGƯỜI CHƠI ---")
	if not inv:
		print("Kho vũ khí hiện đang trống.")
		print("Vui lòng rèn vũ khí bằng Chức năng 2 hoặc Chức năng 3.")
		return
	print("STT | Tên vũ khí                 | Loại        | Cấp | Sát thương tổng")
	print("-" * 80)
	for i, item in enumerate(inv, start=1):
		if isinstance(item, MagicSword):
			typ = "MagicSword"
		elif isinstance(item, Weapon):
			typ = "Weapon"
		else:
			typ = item.__class__.__name__
		dmg = int(item.calculate_total_damage())
		name = getattr(item, 'name', 'Unknown')
		level = getattr(item, 'upgrade_level', '-')
		print(f"{i:3} | {name:26} | {typ:11} | {str(level):4} | {dmg:14}")


def craft_weapon(inv: List[Equipment]) -> None:
	print("\n--- RÈN VŨ KHÍ VẬT LÝ ---")
	name = input("Nhập tên vũ khí: ").strip()
	try:
		base = int(input("Nhập sát thương gốc: ").strip())
		if base <= 0:
			print("Giá trị phải lớn hơn 0!")
			return
	except ValueError:
		print("Giá trị phải là số nguyên!")
		return
	try:
		level = int(input("Nhập cấp cường hóa: ").strip())
		if level <= 0:
			print("Giá trị phải lớn hơn 0!")
			return
	except ValueError:
		print("Giá trị phải là số nguyên!")
		return
	w = Weapon(name, base, level)
	inv.append(w)
	print("\n>> Rèn vũ khí vật lý thành công!")
	print(f"Tên vũ khí: {w.name}")
	print("Loại: Weapon")
	print(f"Cấp cường hóa: {w.upgrade_level}")
	print(f"Sát thương tổng: {int(w.calculate_total_damage())}")


def craft_magic_sword(inv: List[Equipment]) -> None:
	print("\n--- RÈN KIẾM MA THUẬT ---")
	name = input("Nhập tên kiếm ma thuật: ").strip()
	try:
		base = int(input("Nhập sát thương gốc: ").strip())
		if base <= 0:
			print("Giá trị phải lớn hơn 0!")
			return
	except ValueError:
		print("Giá trị phải là số nguyên!")
		return
	try:
		level = int(input("Nhập cấp cường hóa: ").strip())
		if level <= 0:
			print("Giá trị phải lớn hơn 0!")
			return
	except ValueError:
		print("Giá trị phải là số nguyên!")
		return
	try:
		mp = int(input("Nhập sức mạnh phép thuật: ").strip())
		if mp <= 0:
			print("Giá trị phải lớn hơn 0!")
			return
	except ValueError:
		print("Giá trị phải là số nguyên!")
		return
	ms = MagicSword(name, base, level, mp)
	inv.append(ms)
	print("\n>> Rèn kiếm ma thuật thành công!")
	print(f"Tên vũ khí: {ms.name}")
	print("Loại: MagicSword")
	print(f"Cấp cường hóa: {ms.upgrade_level}")
	print(f"Sát thương gốc: {ms.base_damage}")
	print(f"Sức mạnh phép thuật: {ms.magic_power}")
	print(f"Sát thương tổng: {int(ms.calculate_total_damage())}")


def appraise_weapons(inv: List[Equipment]) -> None:
	print("\n--- THẨM ĐỊNH VŨ KHÍ ---")
	if len(inv) < 2:
		print("Cần ít nhất 2 vũ khí trong kho để thẩm định!")
		return
	w1 = inv[0]
	w2 = inv[1]
	print("Vũ khí thứ nhất:")
	print(w1.display() if hasattr(w1, 'display') else str(w1))
	print("\nVũ khí thứ hai:")
	print(w2.display() if hasattr(w2, 'display') else str(w2))

	if w1 > w2:
		print(f"\nKết quả: {w1.name} mạnh hơn {w2.name}.")
	elif w1 == w2:
		print("\nKết quả: Hai vũ khí có sức mạnh ngang nhau.")
	else:
		print(f"\nKết quả: {w2.name} mạnh hơn {w1.name}.")


def fuse_weapons(inv: List[Equipment]) -> None:
	print("\n--- DUNG HỢP VŨ KHÍ ---")
	if len(inv) < 2:
		print("Cần ít nhất 2 vũ khí trong kho để dung hợp!")
		return
	w1 = inv[0]
	w2 = inv[1]
	print("Đang dung hợp 2 vũ khí đầu tiên trong kho...")
	print(f"\nVũ khí 1: {w1.name} | Cấp: {getattr(w1,'upgrade_level','-')} | Sát thương: {int(w1.calculate_total_damage())}")
	print(f"Vũ khí 2: {w2.name} | Cấp: {getattr(w2,'upgrade_level','-')} | Sát thương: {int(w2.calculate_total_damage())}")

	new_weapon = None
	if isinstance(w1, Weapon) and isinstance(w2, Weapon):
		# base damage new = sum of base damages
		new_weapon = w1 + w2
	else:
		print("Chỉ có thể dung hợp giữa hai Weapon.")
		return

	if new_weapon is None:
		print("Dung hợp thất bại do kiểu không hợp lệ.")
		return

	# Calculate base damage sum and upgrade levels already done in __add__
	# Remove old two and append new
	removed1 = inv.pop(0)
	removed2 = inv.pop(0)
	inv.append(new_weapon)

	print("\n>> Dung hợp vũ khí thành công!")
	print(f"Đã xóa khỏi kho: {removed1.name}")
	print(f"Đã xóa khỏi kho: {removed2.name}")
	print("\nVũ khí mới: {}".format(new_weapon.name))
	print("Loại: Weapon")
	print(f"Cấp cường hóa: {new_weapon.upgrade_level}")
	print(f"Sát thương tổng: {int(new_weapon.calculate_total_damage())}")


def main():
	inventory: List[Equipment] = []
	while True:
		print("\n===== LÒ RÈN VŨ KHÍ RIKKEI STUDIOS ===================")
		print("1. Xem kho vũ khí & Sát thương tổng")
		print("2. Rèn Vũ khí Vật lý (Tạo Weapon)")
		print("3. Rèn Kiếm Ma Thuật (Tạo MagicSword)")
		print("4. Thẩm định vũ khí (So sánh lớn hơn)")
		print("5. Dung hợp vũ khí (Cộng dồn cấp độ)")
		print("6. Thoát game")
		print("======================================================")
		choice = input("Chọn chức năng (1-6): ").strip()
		if choice == '1':
			print_inventory(inventory)
		elif choice == '2':
			try:
				craft_weapon(inventory)
			except ValueError as e:
				print(str(e))
		elif choice == '3':
			try:
				craft_magic_sword(inventory)
			except ValueError as e:
				print(str(e))
		elif choice == '4':
			appraise_weapons(inventory)
		elif choice == '5':
			fuse_weapons(inventory)
		elif choice == '6':
			print("Thoát Lò Rèn. Hẹn gặp lại Anh hùng!")
			break
		else:
			print("Lựa chọn không hợp lệ. Vui lòng thử lại.")


if __name__ == '__main__':
	main()

