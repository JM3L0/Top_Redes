import pdfplumber

pdf_path = r'C:\Users\jsous\OneDrive\Área de Trabalho\Trabalho 7\Docs\TRABALHO 07 - ÁRVORE DE FALHA .docx.pdf'
out_path = r'C:\Users\jsous\OneDrive\Área de Trabalho\Trabalho 7\pdf_out.txt'

all_text = []
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        all_text.append(f'--- PAGE {i+1} ---\n{text if text else "[sem texto]"}')

with open(out_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(all_text))

print('done')
