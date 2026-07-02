import pdfplumber

for fname, label in [
    (r'C:\Users\jsous\OneDrive\Área de Trabalho\Trabalho 7\Docs\ARTIGO DE INSPIRAÇÃO.pdf', 'inspiracao'),
    (r'C:\Users\jsous\OneDrive\Área de Trabalho\Trabalho 7\Docs\ARTIGO DE ESPELHAMENTO.pdf', 'espelhamento'),
]:
    all_text = []
    with pdfplumber.open(fname) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            all_text.append(f'--- PAGE {i+1} ---\n{text if text else "[sem texto]"}')
    out_path = rf'C:\Users\jsous\OneDrive\Área de Trabalho\Trabalho 7\{label}_text.txt'
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write('\n'.join(all_text))
    print(f'done: {label}')
