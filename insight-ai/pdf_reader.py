import fitz


def extract_text_from_pdf(uploaded_file) -> str:
    file_bytes = uploaded_file.read()
    document = fitz.open(stream=file_bytes, filetype="pdf")

    text = ""

    for page in document:
        text += page.get_text()

    return text.strip()