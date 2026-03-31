from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

# Keep in sync with host token contract for now.
SECRET_KEY = "tpl-app-dev-secret-key-change-in-production"
ALGORITHM = "HS256"

integration_bearer = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class IntegrationPrincipal:
    """Host-provided identity envelope used by AppSpec integration endpoints.

    AppSpec does not own user/role management. Instead, the host application
    resolves identity and roles and forwards them via headers/token.
    """

    subject: str
    user_id: int | None
    role_keys: set[str]

    def has_any_role(self, keys: set[str]) -> bool:
        normalized = {role.upper() for role in self.role_keys}
        return any(key.upper() in normalized for key in keys)


def _parse_roles(raw: str | None) -> set[str]:
    """Parse CSV role keys from host integration header."""
    if not raw:
        return set()
    return {token.strip().upper() for token in raw.split(",") if token.strip()}


def _parse_user_id(raw: str | None) -> int | None:
    """Parse optional host user id from integration header."""
    if raw is None:
        return None
    stripped = raw.strip()
    if not stripped:
        return None
    try:
        value = int(stripped)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Invalid X-AppSpec-User-Id header") from exc
    return value if value > 0 else None


def get_gui_specs_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(integration_bearer),
    x_appspec_user_id: str | None = Header(default=None, alias="X-AppSpec-User-Id"),
    x_appspec_roles: str | None = Header(default=None, alias="X-AppSpec-Roles"),
) -> IntegrationPrincipal:
    """Resolve GUI-spec principal from bearer token + integration headers.

    Contract:
    - `X-AppSpec-User-Id`: optional numeric user id for audit reference fields.
    - `X-AppSpec-Roles`: optional CSV role keys resolved by host app.
    - Bearer token: optional; if present, `sub` becomes `subject`.
    """

    subject = "anonymous"
    if credentials is not None:
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            subject = str(payload.get("sub") or "").strip() or "anonymous"
        except JWTError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc

    user_id = _parse_user_id(x_appspec_user_id)
    role_keys = _parse_roles(x_appspec_roles)
    return IntegrationPrincipal(subject=subject, user_id=user_id, role_keys=role_keys)


def get_integration_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(integration_bearer),
    x_appspec_user_id: str | None = Header(default=None, alias="X-AppSpec-User-Id"),
    x_appspec_roles: str | None = Header(default=None, alias="X-AppSpec-Roles"),
) -> IntegrationPrincipal:
    """Generic integration principal dependency shared across AppSpec features."""
    return get_gui_specs_principal(
        credentials=credentials,
        x_appspec_user_id=x_appspec_user_id,
        x_appspec_roles=x_appspec_roles,
    )

