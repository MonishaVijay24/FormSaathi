from fastapi import APIRouter, Depends, Response
from app.core.deps import require_session
from app.schemas.models import SessionData
from app.services import application_service as svc, pdf_service

router = APIRouter(prefix="/export", tags=["Export & report"])


def _pdf(data: bytes, name: str) -> Response:
    return Response(content=data, media_type="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="{name}"'})


@router.get("/form.pdf", summary="Filled form as a DRAFT PDF (sensitive values masked by default)")
def form_pdf(mask: bool = True, s: SessionData = Depends(require_session)):
    svc.app_of(s)
    return _pdf(pdf_service.form_pdf(s, mask), "formsaathi_draft.pdf")


@router.get("/report.pdf", summary="Readiness report PDF")
def report_pdf(s: SessionData = Depends(require_session)):
    return _pdf(pdf_service.report_pdf(s, svc.evaluate(s)), "formsaathi_report.pdf")


@router.get("/report.json", summary="Readiness report as JSON (same data as /applications/current/validate)")
def report_json(s: SessionData = Depends(require_session)):
    return svc.evaluate(s)
