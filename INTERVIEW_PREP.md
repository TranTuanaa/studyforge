# StudyForge - Ghi chú phỏng vấn

## 1. Dự án này là gì?

StudyForge là backend viết bằng FastAPI để quản lý dữ liệu học tập và phân bổ thời gian tự học theo tuần.

Người dùng có thể:

- tạo danh sách môn học
- lưu lịch học cố định trên lớp
- lưu các khung thời gian bận cố định như đi làm thêm, tập gym
- import toàn bộ dữ liệu từ CSV
- chạy tối ưu để chia thời gian tự học theo từng ngày
- export kết quả ra CSV

Điểm quan trọng: dự án này tối ưu ở mức "phân bổ số giờ học theo ngày", chưa phải trình xếp lịch chi tiết tới từng mốc giờ cụ thể.

## 2. Cách giới thiệu ngắn gọn khi phỏng vấn

Phiên bản 30 giây:

"Em làm một backend bằng FastAPI tên là StudyForge. Bài toán là nhập môn học, lịch học cố định và các khoảng thời gian bận, sau đó hệ thống tính ra trong tuần còn bao nhiêu thời gian học thực tế và phân bổ số giờ tự học cho từng môn dựa trên độ ưu tiên. Em có làm CRUD, import CSV, export CSV, validation dữ liệu và phần logic tối ưu."

Phiên bản 60-90 giây:

"StudyForge là một backend cá nhân em làm để luyện các phần cốt lõi của backend: thiết kế API, validation, transaction, tổ chức code theo router-service-crud-model-schema, và xử lý business logic. Người dùng có thể nhập danh sách môn học, lịch học trên lớp và các fixed time slots như đi làm thêm hoặc tập gym. Sau đó hệ thống tính free time thật sự trong các study frames đã định nghĩa trước, rồi phân bổ thời gian tự học cho các môn theo priority. Em cũng làm import toàn bộ dữ liệu bằng CSV và rollback toàn bộ nếu có dòng lỗi để tránh dữ liệu nửa vời."

## 3. Bài toán em đang giải

Mục tiêu của hệ thống:

- không chỉ lưu dữ liệu học tập
- mà còn dùng dữ liệu đó để đưa ra một kế hoạch tự học hợp lý theo tuần

Ý tưởng cốt lõi:

- mỗi ngày chỉ có một số khung giờ học nhất định
- lịch học trên lớp và việc bận cố định sẽ chiếm bớt thời gian
- phần thời gian còn lại được chia cho các môn theo priority

## 4. Tech stack và lý do chọn

- FastAPI: viết API nhanh, có Swagger, hợp với project cá nhân backend
- SQLAlchemy: tách model và thao tác database tương đối rõ
- Pydantic v2: validate input/output tốt
- SQLite: đơn giản, nhẹ, đủ cho demo và project cá nhân
- Uvicorn: chạy app FastAPI

Nếu bị hỏi vì sao không dùng PostgreSQL:

"Với scope project cá nhân để tập trung vào API và business logic, em chọn SQLite để giảm setup. Nếu triển khai production hoặc có nhiều người dùng hơn thì em sẽ chuyển sang PostgreSQL."

## 5. Kiến trúc code

Project chia theo các lớp:

- `app/routers/`: định nghĩa endpoint
- `app/schemas/`: validate request và response bằng Pydantic
- `app/models/`: model SQLAlchemy
- `app/crud/`: thao tác dữ liệu cơ bản với database
- `app/services/`: business logic như import CSV và optimization
- `app/core/`: config và helper dùng chung

Luồng xử lý tiêu biểu:

1. request đi vào router
2. schema kiểm tra dữ liệu
3. router gọi CRUD hoặc service
4. CRUD/service thao tác với database
5. response trả về theo schema

## 6. Những file quan trọng nên nhớ

- `app/main.py`: khởi tạo FastAPI, middleware, router, health check
- `app/core/config.py`: đọc cấu hình môi trường
- `app/core/study_frames.py`: định nghĩa các khung giờ học chuẩn
- `app/services/import_service.py`: xử lý import CSV và rollback khi lỗi
- `app/services/optimization_service.py`: phần thuật toán chính
- `app/routers/optimization.py`: lấy dữ liệu từ DB rồi gọi service để tối ưu
- `app/routers/export_schedule.py`: export kết quả tối ưu ra CSV

## 7. Thuật toán chạy như thế nào?

### Mục tiêu của thuật toán

Từ dữ liệu môn học + lịch bận, tính ra:

- tổng thời gian tự học thật sự còn lại trong tuần
- mỗi môn nên được bao nhiêu giờ
- phân bổ số giờ đó vào từng ngày

### Bước 1: định nghĩa study frames

Hệ thống chỉ tính thời gian học trong 3 khung:

- 07:00 - 11:00
- 13:00 - 17:00
- 19:00 - 22:00

Tổng mỗi ngày là 11 giờ học tiềm năng.

Lý do:

- đơn giản hóa bài toán
- tránh phải tối ưu trên cả 24 giờ
- dễ giải thích và dễ debug

### Bước 2: tính thời gian bận thật sự trong các study frames

Từ `class_schedules` và `fixed_time_slots`, hệ thống:

- lấy từng khoảng thời gian bận
- cắt phần giao nhau với các study frames
- gộp các đoạn bị chồng lắp trong cùng một ngày
- trừ phần đã bị chiếm khỏi tổng thời gian học của ngày đó

Điểm cần nhấn mạnh:

- em có xử lý việc các khoảng bận bị overlap để không bị trừ giờ hai lần
- như vậy free time tính ra đúng hơn

### Bước 3: tính tổng free time của cả tuần

Sau khi có free time từng ngày, hệ thống cộng lại để ra `real_free_time`.

Ví dụ:

- Thứ 2 còn 9 giờ
- Thứ 3 còn 10 giờ
- ...
- tổng cả tuần có thể còn 65 giờ

### Bước 4: chia tổng số giờ theo priority

Mỗi môn có `priority`.

Thuật toán:

- cộng toàn bộ priority
- lấy tỷ lệ priority của từng môn
- nhân với tổng số giờ còn lại
- làm tròn theo bước 0.5 giờ để lịch nhìn tự nhiên hơn

Ví dụ:

- Math priority 8
- Physics priority 4
- tổng là 12
- Math nhận khoảng 2/3 tổng thời gian
- Physics nhận khoảng 1/3 tổng thời gian

### Bước 5: phân bổ giờ vào từng ngày

Sau khi biết mỗi môn cần bao nhiêu giờ, hệ thống phân bổ dần vào các ngày còn thời gian trống.

Cách làm:

- dùng bước nhảy 0.5 giờ
- duyệt theo thứ tự priority cao đến thấp
- phân đều qua các ngày còn trống theo kiểu round-robin

Lý do chọn cách này:

- dễ hiểu
- kết quả ổn định, deterministic
- đủ hợp lý cho scope project cá nhân
- không cần kéo thêm thư viện tối ưu nặng

## 8. Dữ liệu được quản lý như thế nào?

### Subject

Thông tin gồm:

- tên môn
- số tín chỉ
- độ khó
- độ ưu tiên

Hiện tại thuật toán đang dùng `priority` để phân bổ giờ. `credits` và `difficulty` được lưu lại để mở rộng sau, ví dụ tạo công thức weight tốt hơn.

### ClassSchedule

Lưu:

- môn học
- thứ trong tuần
- giờ bắt đầu
- giờ kết thúc
- phòng học

### FixedTimeSlot

Lưu các khoảng bận cố định như:

- gym
- part-time job
- hoạt động cá nhân khác

Các fixed slot được validate để nằm trong các study frames, vì mục tiêu của chúng là trừ vào quỹ giờ học.

## 9. Phần import CSV có gì đáng nói?

Đây là điểm tốt để kể khi phỏng vấn vì nó thể hiện em xử lý input thực tế chứ không chỉ CRUD cơ bản.

Những gì import CSV đang làm:

- chỉ nhận file `.csv`
- đọc UTF-8
- kiểm tra header và dữ liệu
- validate từng dòng theo từng loại `subject`, `class_schedule`, `fixed_time`
- có thể map `class_schedule` theo `subject_id` hoặc `subject_name`
- nếu có lỗi ở bất kỳ dòng nào thì rollback toàn bộ transaction

Câu nói gọn:

"Em muốn import phải atomic, tức là hoặc ăn hết, hoặc fail hết, để tránh database rơi vào trạng thái dữ liệu nửa đúng nửa sai."

## 10. Điểm mạnh của project này

- có business logic rõ, không chỉ là CRUD
- chia layer tương đối sạch
- có input validation
- có transaction rollback khi import
- có health check
- có Swagger để demo nhanh
- có export CSV
- thuật toán đủ đơn giản để tự tin giải thích

## 11. Giới hạn hiện tại của project

Đây là phần nên chủ động nói ra, vì nói rõ scope sẽ tạo cảm giác em hiểu sản phẩm của mình.

- kết quả tối ưu là số giờ theo ngày, chưa phải lịch chi tiết tới từng mốc giờ
- chưa có authentication/authorization
- đang dùng SQLite để ưu tiên sự đơn giản
- chưa có test suite hoàn chỉnh
- `credits` và `difficulty` chưa đưa vào công thức phân bổ cuối cùng

Nếu bị hỏi "vì sao chưa làm sâu hơn":

"Em cố ý giữ scope vừa đủ cho một project cá nhân backend. Em ưu tiên làm chắc API, validation, transaction và business logic trước, thay vì ôm quá nhiều thứ rồi cái nào cũng dở."

## 12. Những chỗ interviewer có thể hỏi sâu

### Vì sao em chọn priority thay vì credits hoặc difficulty?

"Vì em muốn phiên bản đầu tiên đơn giản và dễ kiểm chứng. Priority là tín hiệu trực tiếp nhất cho việc phân bổ thời gian. Credits và difficulty em vẫn lưu để có thể mở rộng sang weighted formula ở bản sau."

### Vì sao em không dùng thuật toán tối ưu như linear programming?

"Scope project của em là chứng minh tư duy backend và business logic hơn là nghiên cứu optimization nâng cao. Em chọn một thuật toán deterministic, đủ hợp lý, dễ explain, dễ debug và dễ demo."

### Nếu dữ liệu bị overlap thì sao?

"Em có xử lý merge các đoạn thời gian bận bị chồng lên nhau trong cùng một ngày trước khi trừ quỹ giờ, để tránh bị trừ trùng."

### Vì sao cần rollback khi import?

"Vì nếu một file CSV có 20 dòng mà lỗi ở dòng 19, em không muốn 18 dòng đầu đã ghi xuống DB còn 2 dòng cuối bị fail. Điều đó làm dữ liệu khó tin cậy."

### Vì sao project này đáng gọi là backend project?

"Vì nó có thiết kế API, validate dữ liệu đầu vào, tương tác DB, transaction, tổ chức layer, xử lý file CSV, business logic và export dữ liệu. Nó không chỉ dừng ở CRUD thuần."

## 13. Câu hỏi giả lập và câu trả lời mẫu

### 1. Em hãy giới thiệu dự án của mình

"Dự án của em là StudyForge, một backend hỗ trợ quản lý học tập và phân bổ thời gian tự học theo tuần. Người dùng nhập môn học, lịch học cố định và các khoảng bận, sau đó hệ thống tính free time thực tế trong các khung giờ học và chia số giờ cho từng môn theo độ ưu tiên."

### 2. Khó khăn lớn nhất khi làm là gì?

"Khó khăn lớn nhất là biến dữ liệu thời gian thành logic đủ rõ và không bị rối. Ban đầu nhìn có vẻ chỉ là trừ giờ đơn giản, nhưng khi có nhiều loại block thời gian thì phải chú ý validate input, thời gian chồng lắp, và đảm bảo kết quả không bị trừ trùng."

### 3. Em học được gì từ dự án này?

"Em học được cách chia project backend thành các lớp rõ ràng, cách dùng Pydantic để validate, cách giữ transaction an toàn khi import, và cách biến một bài toán thực tế thành business logic có thể giải thích được."

### 4. Nếu có thêm thời gian em sẽ cải tiến gì?

"Em sẽ thêm test tự động, chuyển sang PostgreSQL, thêm authentication cơ bản, và nâng cấp thuật toán để dùng cả priority, credits, difficulty trong công thức weight. Nếu đi xa hơn nữa thì em sẽ thử xuất ra lịch theo time blocks cụ thể thay vì chỉ theo số giờ mỗi ngày."

### 5. Vì sao em chọn FastAPI?

"Vì FastAPI giúp em viết API nhanh, type hint rõ, validate tốt và có Swagger sẵn nên rất hợp để làm một backend project cá nhân nhưng vẫn chuyên nghiệp."

### 6. Em đã tối ưu gì trong thuật toán?

"Em tối ưu ở mức phù hợp với scope project: giới hạn study frames để bài toán gọn hơn, tính free time thực tế, merge các occupied intervals bị overlap, rồi dùng priority để chia giờ và phân bổ theo bước 0.5 giờ."

### 7. Em xử lý dữ liệu lỗi như thế nào?

"Ở layer schema em validate format cơ bản. Ở import service em parse và validate từng dòng CSV. Nếu có lỗi thì em trả rõ dòng nào bị lỗi và rollback toàn bộ transaction."

## 14. Những câu nên tránh nói

- "Em làm thuật toán AI"
- "Đây là hệ thống tối ưu rất phức tạp"
- "Nó tạo ra lịch hoàn chỉnh như Google Calendar"

Nên nói đúng hơn:

- "Em làm rule-based optimization ở mức phân bổ số giờ"
- "Project tập trung vào backend fundamentals và business logic"
- "Em cố tình giữ scope vừa đủ nhưng làm chắc phần em đã chọn"

## 15. Một số điểm cộng khi demo

Khi demo, nên làm theo flow:

1. vào Swagger
2. tạo 1-2 subject
3. tạo class schedules
4. tạo fixed time slots
5. gọi `POST /optimize/`
6. giải thích vì sao môn priority cao nhận nhiều giờ hơn
7. gọi `POST /export/schedule/`
8. nếu cần, import nhanh bằng `sample_import_all.csv`

## 16. Chốt cách tự tin nhất để nói về project

Điều quan trọng không phải làm dự án quá cao siêu, mà là:

- em hiểu rõ bài toán
- em biết luồng dữ liệu chạy như thế nào
- em giải thích được vì sao code được tổ chức như vậy
- em biết giới hạn hiện tại của hệ thống
- em biết nếu làm tiếp thì sẽ cải tiến ở đâu

Chỉ cần em nói chắc các ý trên, thì đây là một project cá nhân đủ ổn để dùng khi xin intern backend.
