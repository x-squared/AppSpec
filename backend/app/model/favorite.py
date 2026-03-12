from sqlalchemy import Column, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base
from ..enums import FavoriteTypeKey


class Favorite(Base):
    """User-owned quick link to a frequently visited domain entity."""

    __tablename__ = "FAVORITE"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the favorite row.",
        info={"label": "ID"},
    )
    user_id = Column(
        "USER_ID",
        Integer,
        ForeignKey("USER.ID"),
        nullable=False,
        index=True,
        comment="User owning this favorite entry.",
        info={"label": "User"},
    )
    favorite_type_key = Column(
        "FAVORITE_TYPE_KEY",
        SqlEnum(
            FavoriteTypeKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=24,
        ),
        nullable=False,
        index=True,
        comment="Target kind key (PATIENT, EPISODE, COLLOQUIUM, COORDINATION).",
        info={"label": "Favorite Type"},
    )
    name = Column(
        "NAME",
        String(256),
        default="",
        comment="Display name captured for the favorite target.",
        info={"label": "Name"},
    )
    patient_id = Column(
        "PATIENT_ID",
        Integer,
        nullable=True,
        index=True,
        comment="Referenced patient id, if favorite type is PATIENT or EPISODE.",
        info={"label": "Patient"},
    )
    episode_id = Column(
        "EPISODE_ID",
        Integer,
        nullable=True,
        index=True,
        comment="Referenced episode id, if favorite type is EPISODE.",
        info={"label": "Episode"},
    )
    colloqium_id = Column(
        "COLLOQIUM_ID",
        Integer,
        nullable=True,
        index=True,
        comment="Referenced colloquium id, if favorite type is COLLOQUIUM.",
        info={"label": "Colloquium"},
    )
    coordination_id = Column(
        "COORDINATION_ID",
        Integer,
        nullable=True,
        index=True,
        comment="Referenced coordination id, if favorite type is COORDINATION.",
        info={"label": "Coordination"},
    )
    context_json = Column(
        "CONTEXT_JSON",
        Text,
        nullable=True,
        comment="Optional UI context payload (e.g. selected tab) restored when opening the favorite.",
        info={"label": "Context JSON"},
    )
    sort_pos = Column(
        "SORT_POS",
        Integer,
        nullable=False,
        default=0,
        comment="Sort position of the favorite within one user list.",
        info={"label": "Sort Position"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the favorite row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the favorite row.",
        info={"label": "Updated At"},
    )

    user = relationship("User")
