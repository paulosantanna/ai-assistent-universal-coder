"""Authenticated Science Studio routes, installed as app.api.science_studio."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from app.api.deps import Operator, require_operator

router = APIRouter(
    prefix="/api/science-studio", tags=["science-studio"], dependencies=[Depends(require_operator)]
)


def settings():
    path = Path(__file__).with_name("science_studio.json")
    if not path.is_file():
        raise HTTPException(503, "science_studio_not_configured")
    value = json.loads(path.read_text(encoding="utf-8"))
    home = Path(value["home"]).resolve()
    if not (home / "studio.py").is_file():
        raise HTTPException(503, "science_studio_runtime_missing")
    root = Path(value["projects"]).resolve()
    root.mkdir(parents=True, exist_ok=True)
    return value, home, root


def project_path(identifier: uuid.UUID):
    _, _, root = settings()
    folder = root / str(identifier)
    if not (folder / "project.json").is_file():
        raise HTTPException(404, "project_not_found")
    return folder


class NewProject(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str = Field(min_length=3, max_length=500)
    profile: Literal["short", "youtube", "documentary", "full-documentary"] = "short"


class Action(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["generate", "render", "review", "export"]
    checks: list[Literal["science", "visual", "voice", "subtitles", "rights"]] = Field(
        default_factory=list
    )


@router.get("/capabilities")
def capabilities():
    value, home, _ = settings()
    configured = bool(value.get("config") and Path(value["config"]).is_file())
    return {
        "provider_configured": configured,
        "runtime": (home / "studio.py").is_file(),
        "status": "configured_engines_require_preflight"
        if configured
        else "local_models_need_configuration",
        "publishing": False,
    }


@router.get("/projects")
def projects():
    _, _, root = settings()
    items = []
    for path in sorted(root.glob("*/project.json"), key=lambda p: p.stat().st_mtime, reverse=True)[
        :100
    ]:
        try:
            uuid.UUID(path.parent.name)
            project = json.loads(path.read_text(encoding="utf-8"))
            state = path.parent / "job.json"
            items.append(
                {
                    "id": path.parent.name,
                    "topic": project["topic"],
                    "profile": project["profile"],
                    "job": json.loads(state.read_text(encoding="utf-8"))
                    if state.is_file()
                    else {"status": "draft"},
                    "preview": (path.parent / "preview.mp4").is_file(),
                }
            )
        except (ValueError, KeyError, OSError):
            items.append(
                {
                    "id": path.parent.name,
                    "topic": "Projeto indisponível",
                    "profile": "",
                    "job": {"status": "project_unreadable"},
                    "preview": False,
                }
            )
    return {"projects": items}


@router.post("/projects", status_code=201)
def create(body: NewProject):
    _, home, root = settings()
    identifier = uuid.uuid4()
    # Fixed executable/script; user topic is a separate argv value and never shell code.
    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            str(home / "studio.py"),
            "init",
            "--topic",
            body.topic,
            "--profile",
            body.profile,
            "--output",
            str(root / str(identifier)),
        ],
        capture_output=True,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise HTTPException(422, "project_creation_failed")
    return {"id": str(identifier), "status": "draft"}


@router.post("/projects/{identifier}/jobs", status_code=202)
def start(identifier: uuid.UUID, body: Action, operator: Operator):
    value, home, _ = settings()
    folder = project_path(identifier)
    if body.action == "generate" and not (value.get("config") and Path(value["config"]).is_file()):
        raise HTTPException(409, "local_providers_not_configured")
    if body.action == "review" and set(body.checks) != {
        "science",
        "visual",
        "voice",
        "subtitles",
        "rights",
    }:
        raise HTTPException(422, "all_five_review_checks_required")
    lock = folder / ".job.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(descriptor)
    except FileExistsError as exc:
        raise HTTPException(409, "project_job_active_or_interrupted_check_local_worker") from exc
    command = [
        sys.executable,
        str(home / "integration" / "worker.py"),
        str(home),
        str(folder),
        body.action,
    ]
    if body.action == "generate":
        command += ["--config", value["config"]]
    if body.action == "review":
        command += ["--reviewer", str(operator.user.id), "--checks", *body.checks]
    try:
        (folder / "job.json").write_text(
            json.dumps({"status": "queued", "action": body.action}), encoding="utf-8"
        )
        # Fixed worker, UUID-owned folder and allowlisted action; argv is never client-supplied.
        subprocess.Popen(  # noqa: S603
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except OSError as exc:
        lock.unlink(missing_ok=True)
        raise HTTPException(503, "local_worker_start_failed") from exc
    return {"id": str(identifier), "status": "queued"}


@router.get("/projects/{identifier}/files/{name}")
def files(
    identifier: uuid.UUID,
    name: Literal["preview.mp4", "subtitles.srt", "project.json", "approval.json", "final.mp4"],
):
    folder = project_path(identifier)
    path = folder / ("delivery/final.mp4" if name == "final.mp4" else name)
    if not path.is_file():
        raise HTTPException(404, "artifact_not_ready")
    return FileResponse(path)
