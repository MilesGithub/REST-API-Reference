from .crud import init_db, create_user, create_drug, engine
from .auth import get_password_hash
from .models import Drug

def seed():
    init_db()
    # create demo admin + user
    try:
        create_user("admin", get_password_hash("adminpass"), is_admin=True)
    except Exception:
        pass
    try:
        create_user("Joe", get_password_hash("pass123"), is_admin=False)
    except Exception:
        pass
    # sample drugs
    sample = [
        {"name": "Small Molecule 01", "description": "Cardiac support agent.", "atc_code": "C01AA", "indication": "Heart failure", "price_cents": 1299, "in_stock": 500},
        {"name": "Vaccine 01", "description": "Antiviral for respiratory viruses.", "atc_code": "J05AX", "indication": "COVID19", "price_cents": 899, "in_stock": 200},
        {"name": "Monoclonal Antibody 01", "description": "Targeted therapeutic for oncology applications.", "atc_code": "L01XC", "indication": "Cancer", "price_cents": 2499, "in_stock": 150},
    ]
    for d in sample:
        try:
            create_drug(Drug(**d))
        except Exception:
            pass

if __name__ == "__main__":
    seed()
