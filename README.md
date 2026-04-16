# StudyForge - Smart Study Scheduler Backend

**Tối ưu lịch học + nghỉ ngơi theo tuần bằng Linear Programming + Priority Allocation**

Một backend FastAPI giúp sinh viên tự động phân bổ thời gian tự học hợp lý, cân bằng giữa deadline, lịch học trường, fixed time (ngủ, làm thêm, thể thao) và độ ưu tiên của từng môn.

### ✨ Tính năng chính
- CRUD môn học (tên, tín chỉ, độ ưu tiên, độ khó)
- Quản lý lịch học trên trường và fixed time slot (chỉ cho phép trong 3 khung giờ: 7-11, 13-17, 19-22)
- **Tối ưu lịch tự học** thông minh:
  - Tính real free time (trừ lịch học trường + fixed slot)
  - Phân bổ theo % priority 
  - Mỗi môn tối đa 4 tiếng/ngày
- Import môn học từ file **CSV** 
- Export thời khóa biểu ra file **Excel** 

### 🛠 Công nghệ sử dụng
- **FastAPI** (Python)
- **SQLAlchemy 2.0** + Alembic (migrations)
- **PuLP** (Linear Programming - tối ưu)
- **Pydantic v2**
- SQLite (dễ deploy)
- Pandas + Openpyxl (export Excel)
- CORS, Swagger UI

### 🚀 Cách chạy local
```bash
# 1. Clone project
git clone https://github.com/TranTuanaa/studyforge.git
cd studyforge

# 2. Tạo môi trường
py -3.12 -m venv venv
venv\Scripts\activate

# 3. Cài dependencies
pip install -r requirements.txt

# 4. Chạy server
uvicorn app.main:app --reload
```
## Mở Swagger UI: http://127.0.0.1:8000/docs
## 📌 API chính

 - POST /optimize/ → Tối ưu lịch học
 - POST /import/subjects/ → Import từ CSV
 - POST /export/schedule/ → Tải Excel thời khóa biểu
 - CRUD cho Subject, FixedTimeSlot, ClassSchedule

## 📸 Demo

 - Swagger UI: http://127.0.0.1:8000/docs
 - Deploy live: https://studyforge-cn7l.onrender.com/docs

## Tác giả
 - Trần Anh Tuấn
 - Sinh viên Toán Ứng dụng năm 4 Đại học Tôn Đức Thắng (TDTU)
 - Backend Python Developer