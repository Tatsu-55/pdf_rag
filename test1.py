from langchain_community.document_loaders import PyPDFLoader
import test1

#PDFファイルを読み込む
path = "/Users/tatsu/products/pdf_multi_modal_rag/"
filename = "input/test.pdf"
loader = PyPDFLoader(path + filename, extract_images=True)
pages = loader.load_and_split()
print(pages)
print(pages[20].page_content)