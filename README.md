<div align="center">

# Smart Travel Vietnam — AI Travel Assistant  

Nền Tảng AI Tư Vấn & Lên Lịch Trình Du Lịch Thông Minh  

![Travel Logo](https://cdn-icons-png.flaticon.com/512/854/854878.png)

Sử dụng AI để gợi ý điểm đến, đặt tour, tư vấn khách sạn và lên kế hoạch du lịch cá nhân hóa một cách tự động.  

</div>

## 📋 Mục Lục

- [Giới Thiệu](#-giới-thiệu)
- [Tính Năng](#-tính-năng)
- [Công Nghệ](#️-công-nghệ)
- [Kiến Trúc Hệ Thống](#️-kiến-trúc-hệ-thống)
- [Cài Đặt](#-cài-đặt)
- [Sử Dụng](#-sử-dụng)
- [API Documentation](#-api-documentation)
- [Tài Liệu](#-tài-liệu)
- [Đóng Góp](#️-đóng-góp)
- [License](#-license)

---

## 🎯 Giới Thiệu
**Smart Travel AI Assistant** là nền tảng chatbot du lịch thông minh phát triển bởi **Smart Travel Vietnam** — hệ thống hỗ trợ khách hàng khám phá, đặt tour, khách sạn và lên lịch trình du lịch cá nhân hóa.  
Khai thác sức mạnh của **Groq LLM (Llama 3)** kết hợp **LangChain**, hệ thống giúp khách du lịch:

- 🧭 **Tư vấn điểm đến** — Gợi ý địa danh, thời điểm, và gói tour phù hợp sở thích.  
- 🏨 **Gợi ý khách sạn & nhà hàng** — Tìm nơi lưu trú và ăn uống theo ngân sách.  
- 🗓️ **Tự động lên lịch trình** — Xây dựng kế hoạch chi tiết theo số ngày và địa điểm.  
- 📞 **Thu thập thông tin khách hàng** — Lưu họ tên, email, số điện thoại, nơi khởi hành.  
- 📅 **Đặt lịch tư vấn du lịch online** — Hỗ trợ khách hàng trao đổi trực tiếp với nhân viên tư vấn.

🌟 **Điểm Đặc Biệt**
- ✅ **Tư vấn tự động toàn chu trình** – từ khám phá → lập kế hoạch → đặt lịch.  
- ✅ **Ngôn ngữ tự nhiên tiếng Việt** – Hiểu và phản hồi thân thiện.  
- ✅ **Công cụ mạnh mẽ** – `create_booking`, `save_travel_customer`, `save_consultation_schedule_tool`.  
- ✅ **Kết nối MariaDB** – Lưu thông tin khách, gói tour, lịch trình và tư vấn.  

---

## ✨ Tính Năng

🗺️ **1. Tư Vấn Điểm Đến Thông Minh**
- AI hỏi về sở thích (biển, núi, ẩm thực, văn hóa...).  
- Gợi ý địa điểm du lịch trong nước hoặc quốc tế.  
- Hiển thị hình ảnh, mô tả và thời điểm lý tưởng để đi.  

🏨 **2. Gợi Ý Lưu Trú & Ăn Uống**
- Gợi ý khách sạn 3–5 sao, homestay, resort.  
- Đưa ra các quán ăn đặc sản và đánh giá.  

📋 **3. Lên Lịch Trình Du Lịch**
- Lên kế hoạch chi tiết theo ngày (Day 1, Day 2...).  
- Tích hợp thời gian di chuyển và hoạt động.  

🧾 **4. Đặt Tour & Lưu Thông Tin**
- Lưu tour khách chọn vào bảng `bookings`.  
- Thu thông tin khách vào bảng `travel_customers`.  
- Lưu lịch tư vấn vào `consultations`.  

💡 **5. Phân Loại Khách Du Lịch**
- AI gán loại khách:
  - 🟢 Khách tiềm năng (muốn đặt tour sớm)  
  - 🟡 Khách tham khảo (chưa quyết định)  
  - 🔴 Khách không quan tâm  

📅 **6. Đặt Lịch Tư Vấn Online**
- AI đề xuất thời gian tư vấn qua Zalo, Zoom.  
- Gọi tool `save_consultation_schedule_tool` để lưu lịch vào DB.  

🛡️ **7. Bảo Mật & Quản Lý Lỗi**
- Xử lý lỗi API/DB tự động.  
- Hỗ trợ CORS đa miền cho frontend.  
- Ghi log toàn bộ hành vi AI để theo dõi.  

---

## 🛠️ Công Nghệ

| Công Nghệ | Phiên Bản | Mục Đích |
|-----------|-----------|----------|
| [Python](https://python.org) | 3.12+ | Ngôn ngữ chính |
| [FastAPI](https://fastapi.tiangolo.com) | Latest | Web framework |
| [Groq LLM](https://groq.com) | Llama 3 | Xử lý hội thoại |
| [LangChain](https://python.langchain.com) | Latest | Framework AI Agent |
| [Pydantic](https://pydantic.dev) | V2 | Xác thực dữ liệu |
| [MariaDB](https://mariadb.org) | 10+ | Lưu dữ liệu tour & khách hàng |
| [dotenv](https://pypi.org/project/python-dotenv) | Latest | Quản lý biến môi trường |

---

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ index.html│ │ chat.js  │ │ tours.js │ │ booking.js │   │
│  └────┬─────┘  └────┬──────┘  └────┬─────┘  └────┬─────┘   │
│       │              │              │             │         │
│       └──────────────┴──────────────┴─────────────┘         │
│                          │                                  │
│                    Fetch API (HTTP)                         │
└──────────────────────────┼──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    FASTAPI BACKEND                          │
│  ┌────────────────────────────────────────────────────┐     │
│  │  main.py - Agent Executor & Routes                │     │
│  │  • POST /chat                                     │     │
│  │  • OPTIONS /chat (CORS)                           │     │
│  │  • Session & Message Management                   │     │
│  └────┬───────────────────────────┬────────────────┬──┘     │
│       │                           │                │        │
│  ┌────▼─────┐  ┌─────────────────▼──┐  ┌─────────▼──────┐ │
│  │ LangChain│  │ Tools             │  │ Database       │ │
│  │ Agent    │  │ create_booking    │  │ MariaDB        │ │
│  │          │  │ classify_customer │  │ (tours, users) │ │
│  │          │  │ save_consultation │  │                │ │
│  └──────────┘  └───────────────────┘  └──────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

---

## 📦 Cài Đặt

### Yêu Cầu
- Python ≥ 3.12  
- MariaDB ≥ 10  
- [Groq API Key](https://console.groq.com/keys)  

### Bước 1: Clone Repository
```bash
git clone https://github.com/antruong2004/SmartTravelAI.git
cd SmartTravelAI
```

### Bước 2: Tạo Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### Bước 3: Cài Dependencies
```bash
pip install fastapi uvicorn langchain langchain-groq pydantic mysql-connector-python python-dotenv
```

### Bước 4: Tạo Database & .env
**File `.env`:**
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_DATABASE=traveldb
API_KEY=your_groq_api_key
MODEL=llama3-8b-8192
```

### Bước 5: Chạy Server
```bash
uvicorn backend.server:app --reload --host 0.0.0.0 --port 8000
```

---

## 🚀 Sử Dụng

### Test API
```bash
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"input": "Tôi muốn đi Đà Nẵng 3 ngày 2 đêm"}'
```

### Flow Hoạt Động
1. Khách chat → AI gợi ý tour.  
2. AI hiển thị lịch trình mẫu.  
3. AI hỏi thông tin khách → lưu DB.  
4. Nếu khách cần tư vấn → đặt lịch tự động.  

---

## 📖 API Documentation
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
- **Endpoints:**
  - `POST /chat`: Xử lý hội thoại du lịch.  
  - `OPTIONS /chat`: Preflight CORS.  

---

## 📚 Tài Liệu
- [LangChain Tools Setup](docs/LANGCHAIN_SETUP.md)  
- [Database Schema](docs/DB_SCHEMA.md)  
- [API Guide](docs/API_GUIDE.md)

---

## 🤝 Đóng Góp
1. Fork repository  
2. Tạo branch mới (`feature/smart-travel-ai`)  
3. Commit (`git commit -m "Add Smart Travel Assistant feature"`)  
4. Push & tạo Pull Request  

---

## 📄 License
MIT License — xem file LICENSE để biết chi tiết.

---

## 👨‍💻 Tác Giả
**An Trương**  
- GitHub:   
- Email: nvnam160104@gmail.com


🙏 **Acknowledgments**
- [Groq](https://groq.com) — Nền tảng LLM tốc độ cao.  
- [LangChain](https://python.langchain.com) — Framework Agent AI.  
- [FastAPI](https://fastapi.tiangolo.com) — Backend hiệu năng cao.  
- [Smart Travel Vietnam](https://smarttravel.vn) — Đối tác ứng dụng thực tế.

⭐ Nếu project này hữu ích, đừng quên **thả 1⭐ trên GitHub nhé!**
