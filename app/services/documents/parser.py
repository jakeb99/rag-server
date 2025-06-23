import fitz
from io import BytesIO
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.document import InputDocument
from docling.backend.pdf_backend import PdfDocumentBackend



'''
This function parses a pdf file and returns the text from it as a string
'''
async def parse_pdf(file):
    if not file.content_type == "application/pdf":
        return TypeError
    
    content = await file.read()

    doc = fitz.open(stream=content, filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text()
    
    return text

async def parse_pdf_docling(file):
    if not file.content_type == "application/pdf":
        return TypeError
    
    converter = DocumentConverter()
    content = await file.read()

    in_doc = InputDocument(
        path_or_stream=BytesIO(content),
        format=InputFormat.PDF,
        backend=PdfDocumentBackend,
        filename=file.filename
    )
    backend = PdfDocumentBackend(in_doc=in_doc, path_or_stream=BytesIO(content))
    dl_doc = backend.convert()
    print(dl_doc.export_to_markdown())

    # result = converter.convert(in_doc)
    # return result

