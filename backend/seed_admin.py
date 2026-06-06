from app.db.session import SessionLocal
from app.models.models import User
from app.core.security import get_password_hash

def seed_admin():
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Admin user already exists.")
            return

        # Create admin user
        hashed_pw = get_password_hash("admin123")
        admin_user = User(
            username="admin",
            hashed_password=hashed_pw,
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
    except Exception as e:
        print(f"Error seeding admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
