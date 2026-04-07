from langchain_core.tools import tool

# ==========================================
# MOCK DATA - Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Đây là dữ liệu (VD: cuối tuần đặt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu trước khi dùng toolasses.
# ==========================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:30", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "08:15", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_900_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "10:00", "price": 2_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:30", "price": 850_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_200_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_500_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_100_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:20", "arrival": "15:40", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:05", "price": 850_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 8.5},
        {"name": "Sala Đà Nẵng Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 8.2},
        {"name": "Titvicel Beach Hotel", "stars": 3, "price_per_night": 450_000, "area": "Sơn Trà", "rating": 6.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 200_000, "area": "Mỹ Khê", "rating": 7.0},
        {"name": "An Thượng", "stars": 1, "price_per_night": 350_000, "area": "An Thượng", "rating": 6.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Dương Đông", "rating": 8.1},
        {"name": "Bãi Trường", "stars": 3, "price_per_night": 800_000, "area": "Bãi Trường", "rating": 8.0},
        {"name": "Dương Đông", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 6.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 8.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 8.1},
        {"name": "Quận 3", "stars": 3, "price_per_night": 500_000, "area": "Quận 3", "rating": 7.5},
        {"name": "The Common", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 6.4},
    ],
}


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.

    Tham số:
        - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
        - destination: thành phố đích (VD: 'Đà Nẵng', 'Phú Quốc')

    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    key = (origin, destination)
    flights = FLIGHTS_DB.get(key)

    # Thử tra ngược chiều nếu không tìm thấy
    if flights is None:
        reverse_key = (destination, origin)
        flights = FLIGHTS_DB.get(reverse_key)

    if flights is None:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    result = []
    for f in flights:
        price_str = f"{f['price']:,}".replace(",", ".")
        result.append(
            f"- {f['airline']}: {f['departure']} → {f['arrival']} | {price_str}đ | {f['class']}"
        )
    return "\n".join(result)


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.

    Tham số:
        - city: tên thành phố (VD: 'Đà Nẵng', 'Hồ Chí Minh')
        - max_price_per_night: giá tối đa mỗi đêm (VND), mặc định không giới hạn
        - rating: đánh giá sao
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating
    """
    hotels = HOTELS_DB.get(city)

    if hotels is None:
        return f"Không tìm thấy khách sạn tại {city}."

    # Lọc theo giá
    filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]

    if not filtered:
        max_str = f"{max_price_per_night:,}".replace(",", ".")
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {max_str}đ/đêm. Hãy thử tăng ngân sách."

    # Sắp xếp theo rating giảm dần
    filtered.sort(key=lambda h: h["rating"], reverse=True)

    result = []
    for h in filtered:
        price_str = f"{h['price_per_night']:,}".replace(",", ".")
        result.append(
            f"- {h['name']} ({h['stars']}★): {price_str}đ/đêm | {h['area']} | Rating: {h['rating']}"
        )
    return "\n".join(result)


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.

    Tham số:
        - total_budget: tổng ngân sách ban đầu (VND)
        - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy, định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bản chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu
    """
    expense_dict = {}
    items = expenses.split(",")

    for item in items:
        if ":" not in item:
            return f"Lỗi định dạng: '{item}'. Định dạng đúng: 'tên:số_tiền' (VD: 'vé_máy_bay:890000')."
        name, value_str = item.split(":", 1)
        try:
            amount = int(value_str)
        except ValueError:
            return f"Lỗi: số tiền '{value_str}' không hợp lệ."
        expense_dict[name.strip()] = amount

    total_expense = sum(expense_dict.values())
    remaining = total_budget - total_expense

    lines = ["Bảng chi phí:"]
    for name, amount in expense_dict.items():
        amount_str = f"{amount:,}".replace(",", ".")
        lines.append(f"- {name}: {amount_str}đ")

    budget_str = f"{total_budget:,}".replace(",", ".")
    total_str = f"{total_expense:,}".replace(",", ".")

    lines.append("---")
    lines.append(f"Tổng chi: {total_str}đ")
    lines.append(f"Ngân sách: {budget_str}đ")

    if remaining < 0:
        deficit = abs(remaining)
        deficit_str = f"{deficit:,}".replace(",", ".")
        lines.append(f"Còn lại: -{deficit_str}đ")
        lines.append(f"Vượt ngân sách {deficit_str}đ! Cần điều chỉnh.")
    else:
        remaining_str = f"{remaining:,}".replace(",", ".")
        lines.append(f"Còn lại: {remaining_str}đ")

    return "\n".join(lines)


# Chú ý:
# - search_flights: phải sử lý tuple key, thử tra ngược chiều
# - search_hotels: phải lọc + sắp xếp, không chỉ lookup
# - calculate_budget: phải parse chuỗi, xử lý format lỗi, tính toán thực sự
# 3 tools có MỐI LIÊN HỆ: kết quả flights -> input cho budget -> quyết định hotels
