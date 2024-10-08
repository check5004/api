from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/customers/")
def read_customers(skip: int = 0, limit: int = 10, name: str = "", phone_number: str = "", birth_date: str = "", db: Session = Depends(get_db)):
    """
    顧客一覧を取得します。

    - **skip**: スキップする顧客数（オプション、デフォルト: 0）
    - **limit**: 取得する顧客数の上限（オプション、デフォルト: 10）
    - **name**: 顧客名（オプション）
    - **phone_number**: 電話番号（オプション）
    - **birth_date**: 生年月日（オプション）

    戻り値: 顧客オブジェクトのリスト
    """
    customers = crud.get_customers(db, skip=skip, limit=limit, name=name, phone_number=phone_number, birth_date=birth_date)
    response_customers = [
        {
            "id": customer.id,
            "name": customer.name,
            "phoneNumber": customer.phone_number,
            "birthDate": customer.birth_date.isoformat()
        }
        for customer in customers
    ]
    return {
        "status": "success",
        "message": "顧客一覧を取得しました。" if len(response_customers) > 0 else "顧客が見つかりません。",
        "count": len(response_customers),
        "skip": skip,
        "limit": limit,
        "customers": response_customers
    }

@app.get("/customers/{customer_id}")
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    指定されたIDの顧客情報を取得します。

    - **customer_id**: 取得する顧客のID

    戻り値: 顧客オブジェクト
    エラー: 顧客が見つからない場合は404エラー
    """
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    response_customer = {
        "id": db_customer.id,
        "name": db_customer.name,
        "phoneNumber": db_customer.phone_number,
        "birthDate": db_customer.birth_date.isoformat()
    }
    return {
        "status": "success",
        "message": "顧客情報を取得しました。" if db_customer is not None else "顧客が見つかりません。",
        "customer": response_customer
    }

@app.post("/customers/", response_model=schemas.Customer)
def create_or_update_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """
    顧客を作成、更新、または削除します。

    - **customer**: 顧客オブジェクト（CustomerCreateスキーマ）

    動作:
    - delete_flagがTrueの場合、顧客を削除
    - idがNoneの場合、新規顧客を作成
    - idが指定されている場合、既存の顧客を更新

    戻り値: 作成、更新、または削除された顧客オブジェクト
    エラー: 顧客が見つからない場合は404エラー
    """
    if customer.delete_flag:
        deleted_customer = crud.delete_customer(db, customer_id=customer.id)
        if deleted_customer:
            return deleted_customer
        raise HTTPException(status_code=404, detail="顧客が見つかりません。")
    if customer.id is None:
        return crud.create_customer(db=db, customer=customer)
    else:
        updated_customer = crud.update_customer(db=db, customer=customer)
        if updated_customer:
            return updated_customer
        raise HTTPException(status_code=404, detail="顧客が見つかりません。")