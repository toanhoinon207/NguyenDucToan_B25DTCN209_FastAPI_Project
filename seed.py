from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.models.user import User
from app.models.site import ConstructionSite, SiteMember
from app.models.work_item import WorkItem
from app.models.comment import WorkItemComment
from app.core.security import hash_password

def seed_data():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(
                email = "admin@example.com",
                full_name = "Admin Demo",
                password_hash = hash_password("Admin@123"),
                role = "ADMIN",
                is_active = True
            )
            db.add(admin)

        user = db.query(User).filter(User.email == "user@example.com").first()
        if not user:
            user = User(
                email = "user@example.com",
                full_name = "User Demo",
                password_hash = hash_password("User@123"),
                role = "USER",
                is_active = True
            )
            db.add(user)
        db.flush()
    
        site = db.query(ConstructionSite).filter(ConstructionSite.name == "Công trình Demo").first()
        if not site:
            site = ConstructionSite(
                name = "Công trình Demo",
                description = "Công trình mẫu phục vụ test và demo",
                owner_id = admin.id
            )
            db.add(site)
            db.flush()

        admin_member = db.query(SiteMember).filter(SiteMember.site_id == site.id, SiteMember.user_id == admin.id).first()
        if not admin_member:
            admin_member = SiteMember(
                site_id = site.id,
                user_id = admin.id,
                role = "OWNER"
            )
            db.add(admin_member)

        member = db.query(SiteMember).filter(SiteMember.site_id == site.id, SiteMember.user_id == user.id).first()
        if not member:
            member = SiteMember(
                site_id = site.id,
                user_id = user.id,
                role = "MEMBER"
            )
            db.add(member)

        work_item = db.query(WorkItem).filter(WorkItem.title == "Thi công móng").first()
        if not work_item:
            work_item = WorkItem(
                title = "Thi công móng",
                description = "Thi công phần móng công trình",
                status = "TODO",
                priority = "HIGH",
                site_id = site.id,
                assignee_id = user.id,
                due_date = datetime.now() + timedelta(days = 5)
            )
            db.add(work_item)

        work_item_2 = db.query(WorkItem).filter(WorkItem.title == "Xây tường tầng 1").first()
        if not work_item_2:
            work_item_2 = WorkItem(
                title = "Xây tường tầng 1",
                description = "Xây dựng tường tầng 1",
                status = "IN_PROGRESS",
                priority = "MEDIUM",
                site_id = site.id,
                assignee_id = user.id,
                due_date = datetime.now() + timedelta(days = 5)
            )
            db.add(work_item_2)
        db.commit()
        print("================================")
        print("Seed dữ liệu thành công!")
        print("================================")
        print("ADMIN")
        print("Email: admin@example.com")
        print("Password: Admin@123")
        print()
        print("USER")
        print("Email: user@example.com")
        print("Password: User@123")
        print()
        print("Công trình: Công trình Demo")
        print("Hạng mục: Thi công móng")
        print("Hạng mục: Xây tường tầng 1")
        print("================================")
    except Exception as e:
        db.rollback()
        print("Seed dữ liệu thất bại!")
        print(f"Lỗi: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()