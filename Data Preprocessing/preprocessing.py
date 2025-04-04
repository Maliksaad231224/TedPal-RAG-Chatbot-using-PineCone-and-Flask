import re
import PyPDF2
from fpdf import FPDF

# Open and read the PDF
pdf_file = open('data/TedTalks.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
pdf_pages = len(pdf_reader.pages)

text = ''

# Extract text while preserving structure
for page in range(pdf_pages):
    page_obj = pdf_reader.pages[page]
    extracted_text = page_obj.extract_text()
    
    if extracted_text:  
        text += extracted_text + "\n\n"  # Preserve paragraph breaks

# Remove text inside parentheses ( ) and square brackets [ ]
text = re.sub(r'\([^)]*\)', '', text)  # Remove ( ... )
text = re.sub(r'\[[^]]*\]', '', text)  # Remove [ ... ]

# Detect headings (lines that look like "Title Speaker TEDxEvent") and add proper spacing
text = re.sub(r'(^.*?TEDx.*?$)', r'\n\1\n\n', text, flags=re.MULTILINE)

# Merge broken sentences into full paragraphs while keeping headings intact
text = re.sub(r'(?<!\n)\n(?!\n|TEDx)', ' ', text)  # Fix paragraph line breaks without affecting headings

# Preserve multiple blank lines (ensuring paragraphs are not collapsed)
text = re.sub(r'\n{3,}', '\n\n', text)  # Replace 3+ newlines with 2 newlines

# Create and save a new PDF
pdf = FPDF(format='A4')
pdf.add_page()
pdf.set_font('Arial', size=12)

# Use multi_cell to wrap text properly within A4 size
pdf.multi_cell(0, 7, text)

pdf.output('data/output.pdf')

print("PDF successfully created with proper headings and paragraph formatting.")
