# Construction Management API

RESTful API quản lý công trình xây dựng được xây dựng bằng **FastAPI**, **SQLAlchemy** và **MySQL**.

## 1. Công nghệ sử dụng

* Python
* FastAPI
* SQLAlchemy
* MySQL
* Pydantic
* JWT
* bcrypt
* python-dotenv
* Uvicorn

## 2. Chức năng chính

### Authentication

* Đăng ký tài khoản
* Đăng nhập
* Access Token
* Refresh Token
* Kiểm tra tài khoản đang hoạt động
* Mã hóa mật khẩu bằng bcrypt

### User Management

* Xem thông tin tài khoản hiện tại
* Admin xem danh sách người dùng
* Tìm kiếm người dùng theo email và họ tên
* Lọc người dùng theo trạng thái
* Admin cập nhật trạng thái tài khoản

### Construction Site

* Tạo công trình
* Xem danh sách công trình
* Tìm kiếm công trình theo tên
* Xem chi tiết công trình
* Cập nhật công trình
* Xóa mềm công trình
* Quản lý thành viên công trình

### Member Management

* OWNER thêm MEMBER
* OWNER xóa MEMBER
* Xem danh sách thành viên
* Kiểm tra thành viên đã thuộc công trình khác
* Một MEMBER chỉ thuộc một công trình
* Một OWNER có thể sở hữu nhiều công trình
* Không cho phép xóa OWNER

### Work Item

* Tạo hạng mục thi công
* Xem danh sách hạng mục
* Xem chi tiết hạng mục
* Tìm kiếm hạng mục
* Lọc theo status
* Lọc theo priority
* Lọc theo assignee
* Phân trang
* Sắp xếp theo ngày tạo hoặc hạn hoàn thành
* Cập nhật thông tin hạng mục
* Cập nhật assignee
* Cập nhật status
* Xóa hạng mục
* Một assignee có thể được giao nhiều hạng mục
* Cho phép nhiều WorkItem trùng tên nếu khác assignee

### File Upload

* Upload file đính kèm cho WorkItem
* Hỗ trợ PDF, PNG, JPG, JPEG
* Giới hạn file 50MB
* Kiểm tra extension và MIME type
* Đổi tên file bằng UUID để tránh ghi đè

### Comment / Nhật ký thi công

* Thành viên công trình có thể tạo comment
* Thành viên công trình có thể xem comment
* User ngoài công trình không được xem hoặc tạo comment
* Comment lưu người tạo và thời gian tạo

### Activity Log

Ghi nhận các hoạt động quan trọng:

* Tạo công trình
* Cập nhật công trình
* Xóa công trình
* Thêm thành viên
* Xóa thành viên
* Các thao tác quản lý quan trọng khác

---

## 3. Phân quyền

| Đối tượng | Quyền                                                                         |
| --------- | ----------------------------------------------------------------------------- |
| User      | Đăng nhập, xem tài khoản, quản lý công trình mình tham gia                    |
| Admin     | Các quyền của User + quản lý người dùng                                       |
| OWNER     | Quản lý công trình, thành viên và xóa WorkItem                                |
| MEMBER    | Xem công trình, tạo WorkItem, cập nhật status theo nghiệp vụ, xem/tạo comment |

### Quy tắc MEMBER

Một User có thể:

* Là OWNER của nhiều công trình.
* Là MEMBER của tối đa một công trình.
* Có thể vừa là OWNER của nhiều công trình vừa là MEMBER của một công trình khác.

---

## 4. Cấu trúc project

```text
construction_management/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── dependences/
│   │   └── auth.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── site.py
│   │   ├── work_item.py
│   │   ├── work_item_comment.py
│   │   └── activity_log.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── site.py
│   │   ├── work_item.py
│   │   └── comment.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── site.py
│   │   ├── work_item.py
│   │   ├── comment.py
│   │   └── response.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── site_services.py
│   │   ├── work_item_service.py
│   │   ├── upload_file_service.py
│   │   ├── comment_service.py
│   │   └── log_service.py
│   │
│   ├── utils/
│   │   └── exceptions.py
│   │
│   └── main.py
│
├── uploads/
├── seed.py
├── .env
├── requirements.txt
└── README.md
```

---

## 5. Cài đặt

### Clone project

```bash
git clone <repository-url>
cd construction_management
```

### Tạo virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### Cài đặt dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Cấu hình `.env`

Tạo file `.env`:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/construction_management

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7
```

Thay `password` bằng mật khẩu MySQL của máy.

---

## 7. Database

Tạo database MySQL:

```sql
CREATE DATABASE construction_management;
```

Sau đó cấu hình `DATABASE_URL` trong `.env`.

Project sử dụng SQLAlchemy để tạo các bảng:

```text
users
construction_sites
site_members
work_items
work_item_comments
activity_logs
```

---

## 8. Chạy project

Chạy FastAPI:

```bash
uvicorn app.main:app --reload
```

Server mặc định:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## 9. Seed dữ liệu

Chạy:

```bash
python seed.py
```

Dữ liệu mẫu:

### Admin

```text
Email: admin@example.com
Password: Admin@123
Role: ADMIN
```

### User

```text
Email: user@example.com
Password: User@123
Role: USER
```

### Công trình

```text
Công trình Demo
```

### Work Items

```text
Thi công móng
Xây tường tầng 1
```

---

## 10. API chính

### Authentication

```text
POST /auth/register
POST /auth/login
POST /auth/refresh
```

### Users

```text
GET  /users/me
GET  /users
PUT  /users/{user_id}
```

### Construction Sites

```text
POST   /construction-sites
GET    /construction-sites
GET    /construction-sites/{site_id}
PUT    /construction-sites/{site_id}
PATCH  /construction-sites/{site_id}
DELETE /construction-sites/{site_id}
```

### Members

```text
POST   /construction-sites/{site_id}/members
GET    /construction-sites/{site_id}/members
DELETE /construction-sites/{site_id}/members/{user_id}
```

### Work Items

```text
POST   /work-items/{site_id}/work-items
GET    /work-items/{site_id}/work-items
GET    /work-items/{work_item_id}
PATCH  /work-items/{work_item_id}
DELETE /work-items/{work_item_id}
```

### Upload

```text
POST /work-items/{work_item_id}/upload
```

### Comments

```text
POST /work-items/{work_item_id}/comments
GET  /work-items/{work_item_id}/comments
```

### Health Check

```text
GET /health
```

---

## 11. Authentication

Các API yêu cầu đăng nhập sử dụng:

```text
Authorization: Bearer <access_token>
```

Quy trình:

```text
Register
   ↓
Login
   ↓
Access Token + Refresh Token
   ↓
Bearer Access Token
   ↓
Protected API
```

Khi Access Token hết hạn:

```text
Refresh Token
   ↓
Access Token mới
+ Refresh Token mới
```

---

## 12. Soft Delete

Công trình không bị xóa trực tiếp khỏi database.

Khi gọi:

```text
DELETE /construction-sites/{site_id}
```

hệ thống cập nhật:

```text
is_deleted = True
```

Các API lấy danh sách và chi tiết công trình chỉ lấy:

```text
is_deleted = False
```

Điều này giúp giữ lại dữ liệu công trình và Activity Log.

---

## 13. Upload File

Các loại file được phép:

```text
.pdf
.png
.jpg
.jpeg
```

Dung lượng tối đa:

```text
50 MB
```

Tên file được tạo bằng UUID:

```text
550e8400-e29b-41d4-a716-446655440000.pdf
```

Điều này tránh trường hợp nhiều người upload file có cùng tên gây ghi đè.

---

## 14. Error Response

Các HTTPException được chuẩn hóa về format:

```json
{
    "success": false,
    "message": "Bạn không có quyền thực hiện thao tác này",
    "data": null
}
```

Response thành công có thể có dạng:

```json
{
    "success": true,
    "message": "Thao tác thành công",
    "data": {}
}
```

---

## 15. Kiểm thử

Project được kiểm thử các nhóm chức năng:

```text
Authentication
User Management
Construction Site
Site Member
Work Item
File Upload
Comment
Activity Log
Authorization
Validation
Exception Handling
Health Check
```

Các trường hợp kiểm thử bao gồm:

* Request thành công.
* Request không có token.
* Token không hợp lệ.
* Token hết hạn.
* Không đủ quyền.
* Resource không tồn tại.
* User không thuộc công trình.
* MEMBER thuộc công trình khác.
* File không hợp lệ.
* File vượt quá 50MB.
* Dữ liệu đầu vào không hợp lệ.
* Soft delete.
* Phân quyền OWNER/MEMBER/ADMIN.

---

## 16. HTTP Status Code

| Status | Ý nghĩa                            |
| ------ | ---------------------------------- |
| 200    | Thành công                         |
| 201    | Tạo thành công                     |
| 400    | Dữ liệu hoặc request không hợp lệ  |
| 401    | Chưa xác thực / token không hợp lệ |
| 403    | Không có quyền                     |
| 404    | Không tìm thấy tài nguyên          |
| 413    | File vượt quá giới hạn             |
| 422    | Validation thất bại                |

---

## 17. Health Check

Kiểm tra API:

```http
GET /health
```

Response:

```json
{
    "success": true,
    "message": "API đang chạy",
    "data": {
        "status": "OK"
    }
}
```

---

## 18. Tác giả

**Construction Management API**
Project phục vụ mục đích học tập và thực hành xây dựng RESTful API với FastAPI, SQLAlchemy, MySQL, JWT Authentication và RBAC.
