from sqlalchemy import Boolean, Column, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base
from ..enums import PriorityKey, TaskKindKey, TaskScopeKey, TaskStatusKey


class TaskGroupTemplate(Base):
    """Reusable blueprint for creating task groups in a defined transplant scope."""

    __tablename__ = "TASK_GROUP_TEMPLATE"
    __table_args__ = (UniqueConstraint("KEY"),)

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the task group template.",
        info={"label": "ID"},
    )
    key = Column(
        "KEY",
        String(64),
        nullable=False,
        comment="Stable technical key of the task group template.",
        info={"label": "Key"},
    )
    name = Column(
        "NAME",
        String(128),
        nullable=False,
        comment="Display name of the task group template.",
        info={"label": "Name"},
    )
    description = Column(
        "DESCRIPTION",
        String(512),
        default="",
        comment="Description of the task group template purpose.",
        info={"label": "Description"},
    )
    scope_id = Column(
        "SCOPE_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=False,
        comment="Template scope reference (`CODE.TASK_SCOPE`).",
        info={"label": "Task Scope"},
    )
    scope_key = Column(
        "SCOPE_KEY",
        SqlEnum(
            TaskScopeKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=32,
        ),
        nullable=True,
        comment="Template scope enum key mirror of `scope_id`.",
        info={"label": "Task Scope Key"},
    )
    organ_id = Column(
        "ORGAN_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Optional organ constraint (`CODE.ORGAN`) for template applicability.",
        info={"label": "Template Organ"},
    )
    tpl_phase_id = Column(
        "TPL_PHASE_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Optional transplant phase constraint (`CODE.TPL_PHASE`).",
        info={"label": "TPL Phase"},
    )
    is_active = Column(
        "IS_ACTIVE",
        Boolean,
        default=True,
        comment="Whether the task group template can be instantiated.",
        info={"label": "Is Active"},
    )
    sort_pos = Column(
        "SORT_POS",
        Integer,
        default=0,
        comment="Sort position of the template.",
        info={"label": "Sort Position"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the task group template.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the task group template.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the task group template row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the task group template row.",
        info={"label": "Updated At"},
    )

    scope = relationship("Code", foreign_keys=[scope_id])
    organ = relationship("Code", foreign_keys=[organ_id])
    tpl_phase = relationship("Code", foreign_keys=[tpl_phase_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    task_templates = relationship("TaskTemplate", back_populates="task_group_template", cascade="all, delete-orphan")
    task_groups = relationship("TaskGroup", back_populates="task_group_template")


class TaskTemplate(Base):
    """Reusable task definition copied into concrete tasks during instantiation."""

    __tablename__ = "TASK_TEMPLATE"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the task template.",
        info={"label": "ID"},
    )
    task_group_template_id = Column(
        "TASK_GROUP_TEMPLATE_ID",
        Integer,
        ForeignKey("TASK_GROUP_TEMPLATE.ID"),
        nullable=False,
        index=True,
        comment="Parent task group template reference.",
        info={"label": "Task Group Template"},
    )
    description = Column(
        "DESCRIPTION",
        String(512),
        nullable=False,
        default="",
        comment="Template description copied into concrete task descriptions.",
        info={"label": "Description"},
    )
    comment_hint = Column(
        "COMMENT_HINT",
        String(512),
        nullable=False,
        default="",
        comment="Optional guidance text shown as comment placeholder for this task template.",
        info={"label": "Comment Hint"},
    )
    priority_id = Column(
        "PRIORITY_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=False,
        comment="Default priority reference (`CODE.PRIORITY`).",
        info={"label": "Default Priority"},
    )
    priority_key = Column(
        "PRIORITY_KEY",
        SqlEnum(
            PriorityKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=16,
        ),
        nullable=True,
        comment="Default priority enum key mirror of `priority_id`.",
        info={"label": "Default Priority Key"},
    )
    kind_key = Column(
        "KIND",
        SqlEnum(
            TaskKindKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=16,
        ),
        nullable=False,
        default=TaskKindKey.TASK.value,
        comment="Template item kind (`TASK` or `EVENT`).",
        info={"label": "Task Kind"},
    )
    offset_minutes_default = Column(
        "OFFSET_MINUTES_DEFAULT",
        Integer,
        nullable=True,
        comment="Default due offset in minutes from anchor date/time.",
        info={"label": "Offset Minutes Default"},
    )
    is_active = Column(
        "IS_ACTIVE",
        Boolean,
        default=True,
        comment="Whether the task template is active for instantiation.",
        info={"label": "Is Active"},
    )
    sort_pos = Column(
        "SORT_POS",
        Integer,
        default=0,
        comment="Sort position of the task template within its group template.",
        info={"label": "Sort Position"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the task template.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the task template.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the task template row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the task template row.",
        info={"label": "Updated At"},
    )

    task_group_template = relationship("TaskGroupTemplate", back_populates="task_templates")
    priority = relationship("Code", foreign_keys=[priority_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class TaskGroup(Base):
    """Task group bound to a patient, optionally scoped to episode and phase."""

    __tablename__ = "TASK_GROUP"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the task group.",
        info={"label": "ID"},
    )
    patient_id = Column(
        "PATIENT_ID",
        Integer,
        ForeignKey("PATIENT.ID"),
        nullable=True,
        index=True,
        comment="Optional patient context of the task group.",
        info={"label": "Patient"},
    )
    task_group_template_id = Column(
        "TASK_GROUP_TEMPLATE_ID",
        Integer,
        ForeignKey("TASK_GROUP_TEMPLATE.ID"),
        nullable=True,
        index=True,
        comment="Optional source template used to instantiate this task group.",
        info={"label": "Task Group Template"},
    )
    name = Column(
        "NAME",
        String(128),
        nullable=False,
        default="",
        comment="Display name of the task group.",
        info={"label": "Name"},
    )
    episode_id = Column(
        "EPISODE_ID",
        Integer,
        ForeignKey("EPISODE.ID"),
        nullable=True,
        index=True,
        comment="Optional episode context; if set it must belong to the same patient.",
        info={"label": "Episode"},
    )
    colloqium_agenda_id = Column(
        "COLLOQIUM_AGENDA_ID",
        Integer,
        ForeignKey("COLLOQIUM_AGENDA.ID"),
        nullable=True,
        index=True,
        comment="Optional colloqium agenda origin for this task group.",
        info={"label": "Colloqium Agenda"},
    )
    coordination_id = Column(
        "COORDINATION_ID",
        Integer,
        ForeignKey("COORDINATION.ID"),
        nullable=True,
        index=True,
        comment="Optional coordination context for protocol task groups.",
        info={"label": "Coordination"},
    )
    organ_id = Column(
        "ORGAN_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        index=True,
        comment="Optional organ context (`CODE.ORGAN`) for coordination protocol task groups.",
        info={"label": "Organ"},
    )
    tpl_phase_id = Column(
        "TPL_PHASE_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Optional transplant phase (`CODE.TPL_PHASE`), only allowed when episode is set.",
        info={"label": "TPL Phase"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the task group.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the task group.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the task group.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the task group.",
        info={"label": "Updated At"},
    )

    patient = relationship("Patient", back_populates="task_groups")
    task_group_template = relationship("TaskGroupTemplate", back_populates="task_groups")
    episode = relationship("Episode", back_populates="task_groups")
    colloqium_agenda = relationship("ColloqiumAgenda")
    coordination = relationship("Coordination", back_populates="task_groups")
    organ = relationship("Code", foreign_keys=[organ_id])
    tpl_phase = relationship("Code", foreign_keys=[tpl_phase_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    tasks = relationship("Task", back_populates="task_group", cascade="all, delete-orphan")


class Task(Base):
    """Task entry linked to a task group with ownership, timing, and closure state."""

    __tablename__ = "TASK"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the task.",
        info={"label": "ID"},
    )
    task_group_id = Column(
        "TASK_GROUP_ID",
        Integer,
        ForeignKey("TASK_GROUP.ID"),
        nullable=False,
        index=True,
        comment="Parent task group reference.",
        info={"label": "Task Group"},
    )
    description = Column(
        "DESCRIPTION",
        String(512),
        default="",
        comment="Task description text.",
        info={"label": "Description"},
    )
    priority_id = Column(
        "PRIORITY",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=False,
        comment="Priority reference (`CODE.PRIORITY`) of the task.",
        info={"label": "Task Priority"},
    )
    priority_key = Column(
        "PRIORITY_KEY",
        SqlEnum(
            PriorityKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=16,
        ),
        nullable=True,
        comment="Task priority enum key mirror of `priority_id`.",
        info={"label": "Task Priority Key"},
    )
    assigned_to_id = Column(
        "ASSIGNED_TO",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Optional assignee user reference.",
        info={"label": "Assigned To"},
    )
    until = Column(
        "UNTIL_AT",
        DateTime(timezone=True),
        nullable=False,
        comment="Due date/time of the task.",
        info={"label": "Until"},
    )
    kind_key = Column(
        "KIND",
        SqlEnum(
            TaskKindKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=16,
        ),
        nullable=False,
        default=TaskKindKey.TASK.value,
        comment="Task kind (`TASK` or `EVENT`).",
        info={"label": "Task Kind"},
    )
    event_time = Column(
        "EVENT_TIME_TS",
        DateTime(timezone=True),
        nullable=True,
        comment="Timestamp when an event task actually occurred (may differ from closure timestamp).",
        info={"label": "Event Time"},
    )
    status_id = Column(
        "STATUS",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=False,
        comment="Status reference (`CODE.TASK_STATUS`) of the task.",
        info={"label": "Task Status"},
    )
    status_key = Column(
        "STATUS_KEY",
        SqlEnum(
            TaskStatusKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=16,
        ),
        nullable=True,
        comment="Task status enum key mirror of `status_id`.",
        info={"label": "Task Status Key"},
    )
    closed_at = Column(
        "CLOSED_AT_TS",
        DateTime(timezone=True),
        nullable=True,
        comment="Closure timestamp when task becomes completed or discarded.",
        info={"label": "Closed At"},
    )
    closed_by_id = Column(
        "CLOSED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User reference that closed the task.",
        info={"label": "Closed By"},
    )
    comment = Column(
        "COMMENT",
        String(512),
        default="",
        comment="Free-text comment on task processing.",
        info={"label": "Comment"},
    )
    comment_hint = Column(
        "COMMENT_HINT",
        String(512),
        nullable=False,
        default="",
        comment="Optional guidance text shown as comment placeholder for this task.",
        info={"label": "Comment Hint"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the task.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the task.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the task row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the task row.",
        info={"label": "Updated At"},
    )

    task_group = relationship("TaskGroup", back_populates="tasks")
    priority = relationship("Code", foreign_keys=[priority_id])
    status = relationship("Code", foreign_keys=[status_id])
    assigned_to = relationship("User", foreign_keys=[assigned_to_id], back_populates="assigned_tasks")
    closed_by = relationship("User", foreign_keys=[closed_by_id], back_populates="closed_tasks")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])

    @property
    def closed(self) -> bool:
        status_key = self.status_key or (self.status.key if self.status else None)
        return self.closed_at is not None and status_key in {"COMPLETED", "CANCELLED"}
