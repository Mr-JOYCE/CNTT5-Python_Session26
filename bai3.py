from abc import ABC, abstractmethod
from typing import Union, List


class Champion(ABC):
	"""Abstract base class for all champions.

	Attributes:
		champion_id (str): unique identifier
		name (str): champion name
		base_hp (int): base health
		base_atk (int): base attack
	"""

	def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int):
		self.champion_id = champion_id
		self.name = name
		# Edge case: if <= 0 use default 100
		self.base_hp = base_hp if isinstance(base_hp, (int, float)) and base_hp > 0 else 100
		self.base_atk = base_atk if isinstance(base_atk, (int, float)) and base_atk > 0 else 100

	@abstractmethod
	def calculate_skill_damage(self) -> float:
		"""Return skill damage for this champion (must be implemented by subclasses)."""
		pass

	def get_combat_power(self) -> float:
		"""Compute combat power: base_hp + (skill_damage * 1.5)."""
		return float(self.base_hp) + float(self.calculate_skill_damage()) * 1.5

	def __add__(self, other: Union['Champion', int, float]) -> float:
		"""Allow adding two Champions (sum of combat power) or Champion + number.

		Returns a float representing the combined combat power.
		"""
		if isinstance(other, Champion):
			return self.get_combat_power() + other.get_combat_power()
		elif isinstance(other, (int, float)):
			return self.get_combat_power() + float(other)
		return NotImplemented

	def __radd__(self, other: Union[int, float]) -> float:
		# support sum([...]) starting from 0
		if isinstance(other, (int, float)):
			return float(other) + self.get_combat_power()
		return NotImplemented

	def __gt__(self, other: 'Champion') -> bool:
		if not isinstance(other, Champion):
			return NotImplemented
		return self.get_combat_power() > other.get_combat_power()

	def display_row(self) -> str:
		"""Return a formatted row for table display.

		Subclasses should append their own specific info when printing.
		"""
		return f"{self.champion_id:6} | {self.name:20} | {self.base_hp:5} | {self.base_atk:5} |"


class Warrior(Champion):
	"""Warrior champion with a shield bonus attribute."""

	def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int, shield_bonus: int):
		super().__init__(champion_id, name, base_hp, base_atk)
		self.shield_bonus = shield_bonus if isinstance(shield_bonus, (int, float)) else 0

	def calculate_skill_damage(self) -> float:
		# Sát thương kỹ năng = base_atk * 2 + shield_bonus
		return float(self.base_atk) * 2 + float(self.shield_bonus)

	def display_row(self) -> str:
		power = int(self.get_combat_power())
		return f"{self.champion_id:6} | {self.name:20} | {'Warrior':7} | {self.base_hp:5} | {self.base_atk:5} | Armor: {int(self.shield_bonus):5} | {power:6}"


class Mage(Champion):
	"""Mage champion with ability power multiplier."""

	def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int, ability_power: float):
		super().__init__(champion_id, name, base_hp, base_atk)
		self.ability_power = ability_power if isinstance(ability_power, (int, float)) else 1.0

	def calculate_skill_damage(self) -> float:
		# Sát thương kỹ năng = base_atk * ability_power
		return float(self.base_atk) * float(self.ability_power)

	def display_row(self) -> str:
		power = int(self.get_combat_power())
		return f"{self.champion_id:6} | {self.name:20} | {'Mage':7} | {self.base_hp:5} | {self.base_atk:5} | Mana: {int(self.ability_power*100):5} | {power:6}"


def create_default_pool() -> List[Champion]:
	"""Create an initial champion pool with at least 2 Warriors and 1 Mage."""
	return [
		Warrior("WAR01", "Rikkei Knight", 1200, 300, 150),
		Warrior("WAR02", "Steel Guardian", 1500, 250, 200),
		Mage("MAG01", "Rikkei Wizard", 800, 500, 1.5),
	]


def display_champion_pool(pool: List[Champion]) -> None:
	print("--- DANH SÁCH QUÂN CỜ TRONG BỂ TƯỚNG ---")
	print("Mã     | Tên tướng             | Hệ       | HP    | ATK   | Chỉ số riêng       | Chiến lực")
	print("-" * 101)
	for c in pool:
		print(c.display_row())
	print("-" * 101)


def find_champion_by_id(pool: List[Champion], cid: str) -> Union[Champion, None]:
	cid = cid.strip()
	for c in pool:
		if c.champion_id.upper() == cid.upper():
			return c
	return None


def input_positive_number(prompt: str, default: int = 100) -> int:
	while True:
		val = input(prompt).strip()
		try:
			num = float(val)
			if num <= 0:
				print(f"Giá trị phải > 0; đặt mặc định {default}.")
				return default
			return int(num)
		except ValueError:
			print("Giá trị không hợp lệ. Vui lòng nhập một số.")


def add_champion_interactive(pool: List[Champion]) -> None:
	print("Chọn hệ tướng: 1 - Warrior, 2 - Mage")
	choice = input("Lựa chọn (1/2): ").strip()
	if choice not in ("1", "2"):
		print("Lựa chọn không hợp lệ.")
		return

	cid = input("Nhập mã tướng: ").strip()
	if find_champion_by_id(pool, cid):
		print(f"Mã tướng {cid} đã tồn tại. Từ chối thêm.")
		return

	name = input("Nhập tên tướng: ").strip() or "Unknown"
	base_hp = input_positive_number("Nhập HP: ")
	base_atk = input_positive_number("Nhập ATK: ")

	if choice == "1":
		shield = input_positive_number("Nhập Armor: ", default=0)
		champ = Warrior(cid, name, base_hp, base_atk, shield)
	else:
		# ability_power can be float; try parse
		while True:
			ap = input("Nhập Ability Power (ví dụ 1.5): ").strip()
			try:
				apv = float(ap)
				break
			except ValueError:
				print("Giá trị không hợp lệ. Nhập số thực, ví dụ 1.5")
		champ = Mage(cid, name, base_hp, base_atk, apv)

	pool.append(champ)
	print(f"Thêm tướng thành công! Mã: {champ.champion_id} | Tên: {champ.name} | Chiến lực: {int(champ.get_combat_power())}")


def compare_champions_interactive(pool: List[Champion]) -> None:
	print("--- SO SÁNH SỨC MẠNH 2 QUÂN CỜ ---")
	cid1 = input("Nhập mã tướng thứ nhất: ").strip()
	cid2 = input("Nhập mã tướng thứ hai: ").strip()
	c1 = find_champion_by_id(pool, cid1)
	c2 = find_champion_by_id(pool, cid2)
	if not c1:
		print(f"Mã tướng {cid1} không hợp lệ, bỏ qua!")
	if not c2:
		print(f"Mã tướng {cid2} không hợp lệ, bỏ qua!")
	if not c1 or not c2:
		return

	print("Thông tin so sánh:")
	print(f"{c1.champion_id} - {c1.name} | Hệ: {c1.__class__.__name__} | Chiến lực: {int(c1.get_combat_power())}")
	print(f"{c2.champion_id} - {c2.name} | Hệ: {c2.__class__.__name__} | Chiến lực: {int(c2.get_combat_power())}")
	if c1 > c2:
		print(f"Kết quả: {c1.champion_id} - {c1.name} mạnh hơn {c2.champion_id} - {c2.name}.")
	else:
		print(f"Kết quả: {c2.champion_id} - {c2.name} mạnh hơn {c1.champion_id} - {c1.name}.")


def compute_team_power_interactive(pool: List[Champion]) -> None:
	print("--- TÍNH TỔNG CHIẾN LỰC ĐỘI HÌNH RA SÂN ---")
	s = input("Nhập danh sách mã tướng, cách nhau bằng dấu phẩy: ").strip()
	ids = [x.strip() for x in s.split(",") if x.strip()]
	team = []
	for i, cid in enumerate(ids, start=1):
		c = find_champion_by_id(pool, cid)
		if not c:
			print(f"Mã tướng {cid} không hợp lệ, bỏ qua!")
			continue
		team.append(c)

	if not team:
		print("Không có tướng hợp lệ trong đội hình.")
		return

	print("Danh sách đội hình:")
	for idx, c in enumerate(team, start=1):
		print(f"{idx}. {c.champion_id} - {c.name} | Chiến lực: {int(c.get_combat_power())}")

	# sum uses __radd__ and __add__ implementations
	total = sum(team, 0.0)
	print(f"Tổng chiến lực đội hình: {int(total)}")


def main():
	pool = create_default_pool()
	while True:
		print("\n=== Rikkei RPG - Auto-Battler Manager ===")
		print("1. Hiển thị bể tướng")
		print("2. Thêm quân cờ mới")
		print("3. So sánh 2 quân cờ")
		print("4. Tính tổng chiến lực đội hình")
		print("5. Thoát")
		choice = input("Chọn chức năng (1-5): ").strip()
		if choice == "1":
			display_champion_pool(pool)
		elif choice == "2":
			add_champion_interactive(pool)
		elif choice == "3":
			compare_champions_interactive(pool)
		elif choice == "4":
			compute_team_power_interactive(pool)
		elif choice == "5":
			print("Cảm ơn bạn đã sử dụng Rikkei RPG - Auto-Battler Manager!")
			break
		else:
			print("Lựa chọn không hợp lệ. Vui lòng thử lại.")


if __name__ == "__main__":
	main()

