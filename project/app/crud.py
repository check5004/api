from sqlalchemy.orm import Session
from . import models, schemas

def get_customers(db: Session, skip: int = 0, limit: int = 10, name: str = "", phone_number: str = "", birth_date: str = ""):
    return db.query(models.Customer) \
        .filter(models.Customer.name.like(f"%{name}%")) \
        .filter(models.Customer.phone_number.like(f"%{phone_number}%")) \
        .filter(models.Customer.birth_date.like(f"%{birth_date}%")) \
        .offset(skip) \
        .limit(limit) \
        .all()

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer) \
        .filter(models.Customer.id == customer_id) \
        .first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(name=customer.name, phone_number=customer.phone_number, birth_date=customer.birth_date)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = db.query(models.Customer) \
        .filter(models.Customer.id == customer.id) \
        .first()
    if db_customer:
        for key, value in customer.dict(exclude={'id'}).items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    return None

def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(models.Customer) \
        .filter(models.Customer.id == customer_id) \
        .first()
    if db_customer:
        deleted_customer = schemas.Customer(
            id=db_customer.id,
            name=db_customer.name,
            phone_number=db_customer.phone_number,
            birth_date=db_customer.birth_date
        )
        db.delete(db_customer)
        db.commit()
        return deleted_customer
    return None