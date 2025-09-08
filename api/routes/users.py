from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, UserUpdate, UserResponse

router = APIRouter()

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT
SECRET_KEY = "supersecretkey"  # cámbiala por una segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    print('Datos recibidos en registro:', user)
    db_user = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
    if db_user:
            print('Usuario ya existe:', db_user)
            raise HTTPException(status_code=400, detail=f"El usuario '{user.username}' o el email '{user.email}' ya existen")
    hashed_pw = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.email == user.email) | (User.username == getattr(user, "username", None))).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends()):
    # Aquí usarías un método para obtener el usuario actual desde el JWT
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_user_profile(update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends()):
    # Actualizar campos
    current_user.name = update.name or current_user.name
    if update.password:
        current_user.password = get_password_hash(update.password)
    db.commit()
    db.refresh(current_user)
    return current_user
