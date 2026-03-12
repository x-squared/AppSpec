from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session, joinedload

from .audit_context import set_current_changed_by_id
from .database import get_db
from .models import AccessPermission, Code, User

# TODO: move to environment variable
SECRET_KEY = "tpl-app-dev-secret-key-change-in-production"
ALGORITHM = "HS256"

bearer_scheme = HTTPBearer()
PERMISSION_ALIASES: dict[str, str] = {
    "view.donations": "view.donors",
    "edit.donations": "edit.donors",
}


def create_token(ext_id: str) -> str:
    return jwt.encode({"sub": ext_id}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        ext_id: str = payload.get("sub")
        if ext_id is None:
            raise ValueError()
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = (
        db.query(User)
        .options(joinedload(User.role), joinedload(User.roles), joinedload(User.person))
        .filter(User.ext_id == ext_id)
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    set_current_changed_by_id(user.id)
    return user


def get_user_permission_keys(db: Session, user: User) -> list[str]:
    role_ids = set(user.role_ids)
    if not role_ids:
        return []
    keys = (
        db.query(AccessPermission.key)
        .join(AccessPermission.roles)
        .filter(Code.id.in_(role_ids), Code.type == "ROLE")
        .distinct()
        .all()
    )
    permission_keys = {key for (key,) in keys}
    # Backward compatibility: existing DB role mappings may still carry legacy donation keys.
    for legacy_key, canonical_key in PERMISSION_ALIASES.items():
        if legacy_key in permission_keys:
            permission_keys.add(canonical_key)
    return sorted(permission_keys)


def require_permission(permission_key: str):
    def _dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        permissions = set(get_user_permission_keys(db, current_user))
        if permission_key not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {permission_key}",
            )
        return current_user

    return _dependency


def require_admin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    return require_permission("view.admin")(current_user=current_user, db=db)
