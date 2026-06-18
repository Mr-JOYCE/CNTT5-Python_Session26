from abc import ABC, abstractmethod


class Employee(ABC):
	def __init__(self, employee_id: str, name: str):
		self.employee_id = employee_id
		self.name = name

	def display_info(self) -> None:
		employee_type = getattr(self, "employee_type", "Employee")
		print(f"Mã NV: {self.employee_id} | Họ tên: {self.name} | Loại: {employee_type}")

	@abstractmethod
	def calculate_salary(self) -> float:
		raise NotImplementedError()


class FullTimeEmployee(Employee):
	employee_type = "Full-time"

	def __init__(self, employee_id: str, name: str, base_salary: float, bonus: float):
		super().__init__(employee_id, name)
		self.base_salary = base_salary
		self.bonus = bonus

	def calculate_salary(self) -> float:
		return self.base_salary + self.bonus


class PartTimeEmployee(Employee):
	employee_type = "Part-time"

	def __init__(self, employee_id: str, name: str, working_hours: float, hourly_rate: float):
		super().__init__(employee_id, name)
		self.working_hours = working_hours
		self.hourly_rate = hourly_rate

	def calculate_salary(self) -> float:
		return self.working_hours * self.hourly_rate


class InternEmployee(Employee):
	employee_type = "Intern"

	def __init__(self, employee_id: str, name: str, allowance: float):
		super().__init__(employee_id, name)
		self.allowance = allowance

	def calculate_salary(self) -> float:
		return self.allowance


def display_employees(employees: list) -> None:
	print("--- DANH SÁCH NHÂN VIÊN ---")
	for emp in employees:
		emp.display_info()


def display_salaries(employees: list) -> None:
	print("--- BẢNG LƯƠNG NHÂN VIÊN ---")
	for emp in employees:
		salary = emp.calculate_salary()
		salary_str = f"{salary:,.0f} VND"
		# align name column a bit for nicer output
		print(f"{emp.employee_id} | {emp.name.ljust(13)} | Lương: {salary_str}")


def main():
	employees = [
		FullTimeEmployee("E001", "Nguyen Van A", 15000000, 3000000),
		PartTimeEmployee("E002", "Tran Thi B", 80, 50000),
		InternEmployee("E003", "Le Van C", 3000000),
	]

	while True:
		print("\n=== EMPLOYEE SALARY MANAGER ===")
		print("1. Xem danh sách nhân viên")
		print("2. Tính lương toàn bộ nhân viên")
		print("3. Thoát chương trình")
		print("================================")
		choice = input("Chọn chức năng (1-3): ")

		if not choice.isdigit():
			print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
			continue

		choice_num = int(choice)
		if choice_num == 1:
			display_employees(employees)
		elif choice_num == 2:
			display_salaries(employees)
		elif choice_num == 3:
			print("Cảm ơn bạn đã sử dụng Employee Salary Manager!")
			break
		else:
			print("Lựa chọn không hợp lệ. Vui lòng thử lại.")


if __name__ == "__main__":
	main()

