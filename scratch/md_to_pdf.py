import os
from fpdf import FPDF

def clean_text(text):
    return text.encode('ascii', 'ignore').decode('ascii')

def convert_md_to_pdf(md_path, pdf_path):
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found.")
        return

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.set_font("Helvetica", size=11)
    
    in_code_block = False

    for line in lines:
        line = line.rstrip() # keep leading spaces for code
        
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
            
        clean_l = clean_text(line).strip()
        
        if in_code_block:
            pdf.set_font("Courier", size=9)
            if line.strip():
                pdf.multi_cell(180, 5, clean_text(line))
            else:
                pdf.ln(5)
            pdf.set_font("Helvetica", size=11)
            continue

        if not clean_l:
            pdf.ln(2)
            continue

        if clean_l.startswith('# '):
            pdf.set_font("Helvetica", style='B', size=16)
            pdf.multi_cell(180, 10, clean_l[2:])
            pdf.ln(2)
        elif clean_l.startswith('## '):
            pdf.set_font("Helvetica", style='B', size=14)
            pdf.ln(4)
            pdf.multi_cell(180, 10, clean_l[3:])
            pdf.set_font("Helvetica", size=11)
        elif clean_l.startswith('### '):
            pdf.set_font("Helvetica", style='B', size=12)
            pdf.ln(2)
            pdf.multi_cell(180, 8, clean_l[4:])
            pdf.set_font("Helvetica", size=11)
        elif clean_l.startswith('- ') or clean_l.startswith('* '):
            pdf.multi_cell(180, 8, "- " + clean_l[2:])
        elif '|' in clean_l:
            pdf.set_font("Courier", size=8)
            pdf.multi_cell(180, 5, clean_l)
            pdf.set_font("Helvetica", size=11)
        else:
            pdf.multi_cell(180, 8, clean_l)

    pdf.output(pdf_path)
    print(f"Successfully created: {pdf_path}")

if __name__ == "__main__":
    md_file = r"C:\Users\AT\.gemini\antigravity\brain\25bc9573-dc90-4b08-a074-303ce8ae2dc2\artifacts\deep_analysis_sequence_tables.md"
    pdf_file = r"h:\2026\mc_protocol_python\testing\deep_analysis_sequence_tables.pdf"
    convert_md_to_pdf(md_file, pdf_file)
