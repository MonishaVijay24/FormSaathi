from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from app.data.field_library import LIB, GROUPS
from app.schemas.models import SessionData
from app.services.form_mapper import forms
from app.services.text_utils import mask

FOREST, SAFFRON = colors.HexColor("#153A36"), colors.HexColor("#DFA23A")
DISCLAIMER = ("DEMO / FICTIONAL DATA. This is a completed DRAFT for your review. It has NOT been submitted to, "
              "or approved by, any bank, government office or scheme authority.")


def _s(v) -> str:
    """Helvetica is Latin-1 only. Values are transliterated to English; anything else becomes '?'."""
    v = str(v if v is not None else "").replace("₹", "Rs. ")
    return escape(v.encode("latin-1", "replace").decode("latin-1"))


def _mark(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 80)
    canvas.setFillColor(colors.Color(0.92, 0.92, 0.92))
    canvas.translate(A4[0] / 2, A4[1] / 2)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, "DRAFT")
    canvas.restoreState()
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.grey)
    canvas.drawString(15 * mm, 10 * mm, "FormSaathi AI - draft, not submitted or approved")
    canvas.drawRightString(A4[0] - 15 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def _doc(buf):
    return SimpleDocTemplate(buf, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=15 * mm, bottomMargin=18 * mm)


def _table(rows, widths, head=False):
    t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9BFA8")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#FFFAF1"))]
    if head:
        st += [("BACKGROUND", (0, 0), (-1, 0), FOREST), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
    t.setStyle(TableStyle(st))
    return t


def form_pdf(s: SessionData, mask_sensitive: bool = True) -> bytes:
    a, ss = s.application, getSampleStyleSheet()
    form = forms()[a.form_id]
    buf = BytesIO()
    story = [Paragraph(f"<b>{_s(form['title']['en'])}</b>", ss["Title"]),
             Paragraph(_s(DISCLAIMER), ss["Italic"]), Spacer(1, 6 * mm)]
    groups: dict[str, list] = {}
    for fid in a.field_ids:
        f, ans = LIB[fid], a.answers.get(fid)
        val = ans.value if ans and ans.confirmed else "-"
        if mask_sensitive and f["sensitive"] and val != "-":
            val = mask(val)
        groups.setdefault(f["group"], []).append([Paragraph(_s(f["label"]["en"].capitalize()), ss["BodyText"]),
                                                  Paragraph(f"<b>{_s(val)}</b>", ss["BodyText"])])
    for g, rows in groups.items():
        story += [Paragraph(f"<font color='#2C6B5F'><b>{_s(GROUPS[g]['en'])}</b></font>", ss["Heading3"]),
                  _table(rows, [60 * mm, 120 * mm]), Spacer(1, 4 * mm)]
    story += [Spacer(1, 6 * mm), Paragraph("Applicant signature: ____________________   Place / Date: ____________", ss["BodyText"])]
    _doc(buf).build(story, onFirstPage=_mark, onLaterPages=_mark)
    return buf.getvalue()


def report_pdf(s: SessionData, ev: dict) -> bytes:
    ss, buf = getSampleStyleSheet(), BytesIO()
    story = [Paragraph("<b>Application Readiness Report</b>", ss["Title"]), Paragraph(_s(DISCLAIMER), ss["Italic"]),
             Spacer(1, 5 * mm),
             _table([["Readiness", f"{ev['readiness']}%"], ["Total fields", ev["total_fields"]],
                     ["Completed", ev["completed"]], ["Needs review", ev["needs_review"]],
                     ["Issues", ev["issues_count"]]], [60 * mm, 40 * mm]),
             Spacer(1, 3 * mm), Paragraph(_s(ev["note"]), ss["BodyText"]), Spacer(1, 5 * mm),
             Paragraph("<b>Checks that need attention</b>", ss["Heading3"])]
    rows = [["Field", "Status", "You gave", "Document says", "Source", "What to do"]]
    for i in ev["issues"]:
        rows.append([Paragraph(_s(i.field_id), ss["BodyText"]), Paragraph(_s(i.status.replace("_", " ")), ss["BodyText"]),
                     Paragraph(_s(i.form_value or "-"), ss["BodyText"]), Paragraph(_s(i.evidence_value or "-"), ss["BodyText"]),
                     Paragraph(_s(i.source_doc or "-"), ss["BodyText"]), Paragraph(_s(i.message["en"]), ss["BodyText"])])
    story.append(_table(rows, [22 * mm, 24 * mm, 26 * mm, 26 * mm, 22 * mm, 60 * mm], head=True)
                 if len(rows) > 1 else Paragraph("No open issues.", ss["BodyText"]))
    for n in ev["notes"]:
        story += [Spacer(1, 4 * mm), Paragraph(_s("Note: " + n["en"]), ss["BodyText"])]
    story += [Spacer(1, 5 * mm), Paragraph("A text match is not proof of identity or document authenticity.", ss["Italic"])]
    _doc(buf).build(story, onFirstPage=_mark, onLaterPages=_mark)
    return buf.getvalue()
