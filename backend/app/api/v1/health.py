from fastapi import APIRouter

from ...schemas.event import HealthOut

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/healthz", response_model=HealthOut)
def healthz():
    return HealthOut(ok=True)
