"""Authentication router with registration and login using JWT."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(prefix="/auth", tags=["auth"])

def get_password_hash(password: str) -> str:
    """
    Hash a plain password using bcrypt.

    Args:
        password (str): The plain password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed one.

    Args:
        plain_password (str): The user's plain password.
        hashed_password (str): The stored hashed password.

    Returns:
        bool: True if the password is correct, else False.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta, optional): Token expiration time.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Retrieve a user by email.

    Args:
        db (Session): SQLAlchemy session.
        email (str): User email.

    Returns:
        User | None: The user object if found, otherwise None.
    """
    return db.query(User).filter(User.email == email).first()

@router.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        form_data (OAuth2PasswordRequestForm): The user credentials.
        db (Session): SQLAlchemy session.

    Raises:
        HTTPException: If email already exists.

    Returns:
        dict: Success message.
    """
    if get_user_by_email(db, form_data.username):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        name=form_data.username,
        email=form_data.username,
        password_hash=get_password_hash(form_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "User registered"}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): The user credentials.
        db (Session): SQLAlchemy session.

    Raises:
        HTTPException: If credentials are invalid.

    Returns:
        dict: Access token and token type.
    """
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Get the current authenticated user from JWT token.

    Args:
        token (str): JWT token from request header.
        db (Session): SQLAlchemy session.

    Raises:
        HTTPException: If token is invalid or user not found.

    Returns:
        User: Authenticated user.
    """
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
