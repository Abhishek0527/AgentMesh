from pypdf import PdfReader


def load_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    text =""

    for page in reader.pages:
        text+= page.extract_text()


    return text

#print(load_pdf("E:\AgentMesh\rag\data\AI_in_Medicine.pdf"))