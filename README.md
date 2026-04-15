# StudyForge - Smart Study Scheduler Backend

**Công cụ tối ưu lịch tự học thông minh cho sinh viên**  
Sử dụng Linear Programming (PuLP) + FastAPI, phù hợp với sinh viên Toán Ứng dụng.

### ✨ Tính năng nổi bật
- Tính **thời gian rảnh thực tế** (đã trừ lịch học trên trường + fixed activities)
- Chỉ cho phép tự học trong **3 khung giờ cố định**: 7h-11h, 13h-17h, 19h-22h
- Phân bổ thời gian tự học theo **tỷ lệ ưu tiên** (priority)
- Mỗi môn **tối đa 4 tiếng/ngày**
- Validation nghiêm ngặt cho fixed time slot

### 🛠 Công nghệ
- **FastAPI**
- **SQLAlchemy** + Alembic
- **PuLP** (Linear Programming)
- SQLite

### 🚀 Cách chạy local

```bash
git clone https://github.com/TranTuanaa/studyforge.git
cd studyforge

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```
## Swagger UI: http://127.0.0.1:8000/docs
## 📌 API chính

 - POST /subjects/ → Tạo môn học
 - POST /class-schedules/ → Tạo lịch học trên trường
 - POST /fixed-slots/ → Tạo hoạt động cố định (chỉ cho phép trong 3 khung giờ)
 - POST /optimize/ → Tối ưu lịch tự học

## 📝 Tác giả
 - Trần Anh Tuấn sinh viên Toán Ứng dụng năm 4 Đại học Tôn Đức Thắng
