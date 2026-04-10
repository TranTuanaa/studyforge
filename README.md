# StudyForge - Smart Study Scheduler Backend

**Backend cho công cụ tối ưu lịch tự học thông minh**  
Sử dụng Linear Programming + FastAPI + PuLP, dành cho sinh viên Toán Ứng dụng.

### ✨ Tính năng chính
- Tính **thời gian rảnh thực tế** sau khi trừ lịch học trên trường và fixed activities
- Chỉ cho phép tự học trong **3 khung giờ cố định**: 7-11, 13-17, 19-22
- Phân bổ thời gian tự học theo **tỷ lệ priority**
- Mỗi môn **tối đa 4 tiếng/ngày**
- Validation nghiêm ngặt cho fixed time slot (không cho tạo ngoài 3 khung giờ)

### 🛠 Công nghệ sử dụng
- **FastAPI**
- **SQLAlchemy** + Alembic
- **PuLP** (Linear Programming)
- **SQLite** (dễ deploy)
- Python 3.10+

### 🚀 Cài đặt & Chạy

```bash
# 1. Clone project
git clone https://github.com/TranTuanaa/studyforge.git
cd studyforge

# 2. Tạo môi trường
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate # Mac/Linux

# 3. Cài dependencies
pip install -r requirements.txt

# 4. Chạy server
uvicorn app.main:app --reload
```
## Server chạy tại: http://127.0.0.1:8000
## Swagger UI: http://127.0.0.1:8000/docs
## 📌 API chính

 - POST /subjects/ → Tạo môn học
 - POST /class-schedules/ → Tạo lịch học trên trường
 - POST /fixed-slots/ → Tạo hoạt động cố định (chỉ cho phép trong 3 khung giờ)
 - POST /optimize/ → Tối ưu lịch tự học (trả về kết quả chính)

## 📸 Demo kết quả
Objective_value sẽ là thời gian rảnh thực tế (đã trừ lịch học + fixed slot).
Ví dụ output:
JSON{
  "status": "Optimal",
  "objective_value": 66.0,
  "schedule": [ ... ],
  "message": "Thời gian rảnh thực tế: 66.0 tiếng (đã trừ đúng phần trong 3 khung giờ)"
}
##📝 Tác giả

 - Trần Tuấn Anh – Sinh viên Toán Ứng dụng năm 4
 - Project 2 (sau Project Manager API)