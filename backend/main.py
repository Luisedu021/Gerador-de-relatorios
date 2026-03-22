from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fpdf import FPDF

app = FastAPI()

# Permite que o seu Front-end (HTML/JS) converse com este Back-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # DICA: Em produção, coloque o domínio real do site da Mega Jr.
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define o formato dos dados que a API vai receber do Front-end
class DadosAta(BaseModel):
    data_hora: str
    detalhes: str
    pontos_importantes: str
    # No futuro, você pode enviar o resumo já gerado pela IA aqui

@app.post("/api/gerar-pdf")
def gerar_pdf(dados: DadosAta):
    # 1. Inicializa o PDF
    pdf = FPDF()
    pdf.add_page()
    
    # 2. Configura a fonte e o Título
    pdf.set_font("helvetica", style="B", size=16)
    pdf.set_text_color(86, 8, 168) # Roxo da Mega Jr. (#5608A8)
    pdf.cell(0, 10, "Ata de Reunião Inteligente - Mega Jr.", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    
    # 3. Adiciona os dados
    pdf.set_font("helvetica", size=12)
    pdf.set_text_color(0, 0, 0) # Preto para o texto
    
    pdf.set_font("helvetica", style="B", size=12)
    pdf.cell(0, 10, f"Data e Horário:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=12)
    pdf.multi_cell(0, 10, dados.data_hora)
    pdf.ln(5)
    
    pdf.set_font("helvetica", style="B", size=12)
    pdf.cell(0, 10, f"Detalhes da Reunião:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=12)
    pdf.multi_cell(0, 10, dados.detalhes)
    pdf.ln(5)

    pdf.set_font("helvetica", style="B", size=12)
    pdf.cell(0, 10, f"Pontos Importantes:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=12)
    pdf.multi_cell(0, 10, dados.pontos_importantes)

    # 4. Gera o arquivo em memória (bytes)
    pdf_bytes = bytes(pdf.output())

    # 5. Retorna o arquivo como um download
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Resumo_Ata_MegaJr.pdf"}
    )