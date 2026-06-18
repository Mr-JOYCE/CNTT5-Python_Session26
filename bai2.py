# Phân tích lỗi (Code Review)
#
# 1) Vòng lặp `for hero in team_heroes: hero.use_ultimate()` thể hiện tính Đa hình thế nào?
#    - Mỗi đối tượng trong `team_heroes` có cùng giao diện (`use_ultimate()`), nhưng
#      triển khai khác nhau tùy lớp (Mage/Assassin). Vòng lặp gọi cùng một phương thức
#      trên mọi đối tượng mà không cần biết kiểu cụ thể — đó chính là polymorphism
#      (và duck typing) trong Python.
#
# 2) Với code cũ (không dùng `abc`), `Assassin` vẫn được tạo thành công; lỗi NotImplementedError
#    được ném ra vào thời điểm **chạy** vòng lặp gọi `use_ultimate()` (tức lúc giao tranh).
#    Báo lỗi muộn như vậy là tồi tệ vì nó khiến game chỉ crash khi trận đấu đã bắt đầu—
#    trải nghiệm người chơi bị gián đoạn, khó debug, và server có thể rơi vào trạng thái
#    không ổn định trong runtime.
#
# 3) Nếu dùng `abc` + `@abstractmethod`, lỗi sẽ bật ra **khi khởi tạo** lớp con mà chưa
#    override phương thức trừu tượng (tức lúc loading/trước khi trận đấu bắt đầu).
#    Điều này giúp "fail fast"—phát hiện cấu trúc lớp sai ngay lập tức.
#
# 4) Nguyên lý Fail Fast với Abstract Base Classes:
#    - Áp dụng `ABC` và `@abstractmethod` buộc lớp con phải cài đặt các phương thức
#      quan trọng ngay tại thời điểm tạo lớp/khởi tạo instance; nếu không, Python sẽ
#      ngăn không cho khởi tạo (TypeError). Điều này phát hiện lỗi sớm và làm cho
#      hệ thống an toàn hơn.


from abc import ABC, abstractmethod


class Hero(ABC):
	@abstractmethod
	def use_ultimate(self):
		pass


class Mage(Hero):
	def use_ultimate(self):
		print("🔥 Pháp Sư tung chiêu: MƯA SAO BĂNG!")


class Assassin(Hero):
	# Đổi tên từ stealth_kill -> use_ultimate để tuân theo interface
	def use_ultimate(self):
		print("🗡️ Sát Thủ tung chiêu: ÁM SÁT TỪ PHÍA SAU!")


if __name__ == "__main__":
	print("--- LOADING TRẬN ĐẤU ---")
	team_heroes = [Mage(), Assassin()]
	print("Tải trận đấu thành công! Các tướng đã sẵn sàng...")

	print("\n--- GIAO TRANH TỔNG BẮT ĐẦU ---")
	for hero in team_heroes:
		hero.use_ultimate()

