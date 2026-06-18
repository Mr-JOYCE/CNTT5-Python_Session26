# Phân tích lỗi (Code Review)
#
# 1) Tại sao dòng print(f"Chiến binh {w1.name}...") văng AttributeError?
#    - Nguyên nhân: Trong hàm khởi tạo của lớp con `Warrior.__init__` lập trình viên
#      đã không gọi hàm khởi tạo của lớp cha `Character`. Do đó các thuộc tính
#      `name`, `hp`, `attack_power` không được gán lên instance `self` khi tạo
#      đối tượng `Warrior`.
#    - Hậu quả: Khi truy cập `w1.name` Python tìm trên đối tượng `w1` không thấy
#      thuộc tính `name` nên ném `AttributeError: 'Warrior' object has no attribute 'name'`.
#    - Thiếu cú pháp cần thiết: cần gọi `super().__init__(name, hp, attack_power)`
#      trong `Warrior.__init__` để kế thừa và khởi tạo các thuộc tính của lớp cha.
#
# 2) Nếu không dùng super().__init__(...), làm cách nào khác (không khuyến khích)?
#    - Có thể gọi trực tiếp hàm khởi tạo của lớp cha: `Character.__init__(self, name, hp, attack_power)`.
#    - Hoặc tự gán các thuộc tính trong `Warrior.__init__`:
#         self.name = name
#         self.hp = hp
#         self.attack_power = attack_power
#      Cả hai cách trên hoạt động, nhưng đều bỏ qua cơ chế khởi tạo hợp tác
#      (cooperative multiple inheritance) và không được khuyến khích trong các
#      thiết kế có đa kế thừa.
#
# 3) Nếu lỗi 1 đã được sửa, khi chạy `if w1 > w2:` console sẽ in ra Exception gì?
#    - Trong Python 3, nếu lớp không định nghĩa phương thức so sánh cho `>`,
#      phép so sánh `w1 > w2` sẽ gây ra `TypeError: '>' not supported between instances of 'Warrior' and 'Warrior'`.
#    - Lý do: toán tử `>` gọi vào magic method `__gt__`; nếu không có định nghĩa
#      thì Python không biết tiêu chí để so sánh hai đối tượng tùy biến.
#
# 4) Để `>` hoạt động dựa trên `get_total_power()`, cần khai báo dunder method nào?
#    - Cần implement `def __gt__(self, other):` trong lớp `Warrior`.
#    - Số tham số: hai tham số — `self` và `other`.
#    - Nội dung thiết kế:
#         - Nếu `other` không phải `Warrior`, trả về `NotImplemented`.
#         - Trả về kết quả so sánh boolean: `self.get_total_power() > other.get_total_power()`.
#    - Gợi ý bổ sung: nên cân nhắc triển khai cả `__lt__`, `__eq__` (và/hoặc
#      sử dụng `functools.total_ordering`) để có bộ so sánh hoàn chỉnh.


class Character:
	def __init__(self, name, hp, attack_power):
		self.name = name
		self.hp = hp
		self.attack_power = attack_power


class Warrior(Character):
	def __init__(self, name, hp, attack_power, bonus_armor):
		super().__init__(name, hp, attack_power)
		self.bonus_armor = bonus_armor

	def get_total_power(self):
		return self.attack_power + self.bonus_armor

	def __gt__(self, other):
		if not isinstance(other, Warrior):
			return NotImplemented
		return self.get_total_power() > other.get_total_power()


if __name__ == "__main__":
	w1 = Warrior("Arthur", 1000, 150, 50)   # total 200
	w2 = Warrior("Lancelot", 900, 180, 10)  # total 190

	print(f"Chiến binh {w1.name} xuất trận!")

	if w1 > w2:
		print(f"{w1.name} mạnh hơn {w2.name}!")
	else:
		print(f"{w2.name} mạnh hơn hoặc hòa!")

