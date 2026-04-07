# TravelBuddy - Trợ lý Du lịch Thông minh

Một AI agent được xây dựng bằng **LangGraph** và **GPT-4o-mini**, hỗ trợ người dùng lên kế hoạch chuyến đi tại Việt Nam với các tính năng tra cứu chuyến bay, tìm khách sạn, và tính toán ngân sách.

## Cấu trúc Project

```
.
├── agent.py              # Agent graph chính (LangGraph)
├── tools.py              # Các tool: search_flights, search_hotels, calculate_budget
├── system_prompt.txt     # Prompt định nghĩa persona và hành vi agent
├── test_cases.txt        # 5 test case để đánh giá agent
├── requirements.txt      # Dependencies
├── test_results/         # Lịch sử hội thoại (tự động lưu)
└── .env                  # API keys (OpenAI)
```

## Cài đặt

```bash
# Kích hoạt virtual environment
source .venv/bin/activate

# Cài dependencies
pip install -r requirements.txt

# Thêm OpenAI API key vào .env
echo "OPENAI_API_KEY=sk-..." > .env
```

## Chạy Agent

```bash
python agent.py
```

Agent sẽ lưu lịch sử hội thoại vào thư mục `test_results/` sau mỗi lần thoát.

## Các Tool

| Tool | Mô tả |
|------|-------|
| `search_flights` | Tìm chuyến bay theo điểm đi/đến. Hỗ trợ tra ngược chiều. |
| `search_hotels` | Tìm khách sạn theo thành phố, lọc theo giá tối đa, sắp xếp theo rating. |
| `calculate_budget` | Phân bổ ngân sách, trừ chi phí, cảnh báo vượt ngân sách. |

## Luồng Xử lý

Khi người dùng cung cấp điểm đến và ngân sách, agent tự động thực hiện chuỗi 3 bước:

1. **search_flights** → tra chuyến bay phù hợp
2. **calculate_budget** → trừ vé máy bay, tính ngân sách còn lại
3. **search_hotels** → tìm khách sạn trong ngân sách còn lại

## Test Cases

| # | Mô tả | Kỳ vọng |
|---|-------|---------|
| 1 | Chào hỏi, chưa có điểm đến | Trả lời thân thiện, hỏi thêm |
| 2 | Tìm 1 chuyến bay cụ thể | Gọi search_flights |
| 3 | Lên kế hoạch đầy đủ (bay + khách sạn + ngân sách) | Chain 3 tools |
| 4 | Thiếu thông tin ("đặt khách sạn") | Hỏi lại làm rõ |
| 5 | Yêu cầu ngoài phạm vi (code, bài tập) | Từ chối lịch sự |

## Ví dụ

```
Bạn: Tôi ở Hà Nội, ngày mai muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp tôi!

TravelBuddy đang suy nghĩ...
Gọi tool: search_flights(...)
Gọi tool: calculate_budget(...)
Gọi tool: search_hotels(...)

TravelBuddy:
Chuyến bay: Vietnam Airlines 07:00→08:15 | 1.100.000đ | economy
Khách sạn: Sol Beach (4★) | 1.200.000đ/đêm | Dương Đông | Rating: 8.1
Tổng chi phí ước tính: ~3.500.000đ
Gợi ý thêm: Vinpearl Resort có rating thấp (4.4) nên mình không recommend
```

## Dependencies

- `langgraph==1.1.6`
- `langchain-openai==1.1.12`
- `openai==2.30.0`
- Python 3.12+
