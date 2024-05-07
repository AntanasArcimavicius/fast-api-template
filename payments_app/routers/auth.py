from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "thequickbrownfoxjumpsoverthelazydog"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class UserNotFoundException(HTTPException):
    def __init__(self, status_code: int, detail: str = "", headers: dict = {}) -> None:
        super().__init__(status_code, detail, headers)


class CredentialsException(HTTPException):
    def __init__(self) -> None:
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Could not validate credentials"
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code, detail, headers)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool = False


class UserInDB(User):
    hashed_password: str


# password1234
fake_users_db = dict(
    johndoe=dict(
        username="johndoe",
        full_name="Johne Doe",
        email="johndoe@example.com",
        hashed_password="$2b$12$KcJ2OvQZY90SPwuGV9WzdOuCXl.eBzB9YXjkgSDvI2oTbfkSnaMny",
        disabled=False,
    )
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db, username: str) -> UserInDB | None:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

    raise UserNotFoundException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def authenticate_user(fake_db, username: str, password: str) -> UserInDB | None:
    user = get_user(fake_db, username)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise CredentialsException()
        token_data = TokenData(username=username)

    except JWTError:
        raise CredentialsException()

    user = get_user(fake_users_db, username=token_data.username)

    if user is None:
        raise CredentialsException()

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user


@router.post("/token", response_model=Token, tags=["auth"], include_in_schema=False)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)

    if not user:
        raise UserNotFoundException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
