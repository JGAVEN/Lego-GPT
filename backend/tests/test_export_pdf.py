import tempfile
from pathlib import Path
import backend.export as export


def test_ldr_to_pdf():
    with tempfile.TemporaryDirectory() as tmp:
        ldr = Path(tmp) / "model.ldr"
        ldr.write_text("0 FILE model.ldr")
        pdf = Path(tmp) / "out.pdf"
        export.ldr_to_pdf(ldr, pdf)
        assert pdf.is_file()
