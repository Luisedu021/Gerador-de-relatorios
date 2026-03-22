from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fpdf import FPDF
import os
from dotenv import load_dotenv
from google import genai

# 1. Carrega as senhas do arquivo .env
load_dotenv()

# 2. Configura o cliente do Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ==========================================
# DEFINIÇÃO DO PADRÃO DO PDF (Design Mega)
# ==========================================
class MegaJrPDF(FPDF):
    def load_custom_fonts(self):
        """Carrega a Montserrat. Certifique-se de ter os arquivos TTF na pasta 'fonts'"""
        fonts_path = "fonts"
        regular_font = os.path.join(fonts_path, "Montserrat-Regular.ttf")
        bold_font = os.path.join(fonts_path, "Montserrat-Bold.ttf")

        if os.path.exists(regular_font) and os.path.exists(bold_font):
            self.add_font("Montserrat", "", regular_font, uni=True)
            self.add_font("Montserrat", "B", bold_font, uni=True)
            return True
        else:
            print("⚠️ AVISO: Arquivos Montserrat TTF não encontrados. Usando Helvetica padrão.")
            return False

    def footer(self):
        """Essa função é chamada automaticamente ao final de CADA página"""
        self.set_y(-15)
        
        try:
            self.set_font("Montserrat", "", 8)
        except:
            self.set_font("helvetica", "", 8)
            
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "Ata gerada automaticamente pela MEGA IA.", align="L")
        
        self.set_fill_color(255, 222, 89)
        self.rect(0, 290, 210, 7, style="F")
        
        self.set_y(-7)
        try:
            self.set_font("Montserrat", "B", 8)
        except:
            self.set_font("helvetica", "B", 8)
            
        self.set_text_color(0, 0, 0)
        self.cell(0, 5, f'Página {self.page_no()}/{{nb}}', align='C')


# ==========================================
# INICIALIZAÇÃO DA API (FastAPI)
# ==========================================
app = FastAPI() # <-- O SEU TERMINAL ESTAVA PROCURANDO ISSO AQUI!

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class DadosAta(BaseModel):
    data_hora: str
    detalhes: str
    pontos_importantes: str

@app.post("/api/gerar-pdf")
def gerar_pdf(dados: DadosAta):
    instrucao = f"""

    ⚠️ REGRA DE SEGURANÇA MÁXIMA:
    Avalie o texto fornecido pelo usuário. Se ele for apenas letras aleatórias sem sentido (ex: "asdasdasd", "kjdfhgk"), xingamentos, ou não contiver absolutamente nenhuma informação real de uma reunião, você DEVE abortar a missão e responder EXATAMENTE e APENAS com a palavra: ERRO_TEXTO_INVALIDO. Não explique o motivo, apenas devolva essa palavra.
    
    Você é um assistente executivo sênior da Mega Jr., uma empresa júnior de tecnologia.
    Sua tarefa é organizar e melhorar a escrita das anotações de uma reunião.
    
    Anotações cruas:
    - Detalhes: {dados.detalhes}
    - Pontos Soltos: {dados.pontos_importantes}
    
    Por favor, crie um "Resumo Executivo" profissional e direto ao ponto (máximo de 4 parágrafos).
    Em seguida, liste as "Ações Definidas" (próximos passos) em bullet points.
    Não use formatação Markdown (como ** ou #), apenas texto limpo.
    """
    
    resposta_ia = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=instrucao,
    )
    texto_processado = resposta_ia.text
    
    pdf = MegaJrPDF()
    pdf.alias_nb_pages()

    using_montserrat = pdf.load_custom_fonts()
    font_family = "Montserrat" if using_montserrat else "helvetica"

    pdf.add_page()
    
    try:
        pdf.image("assets/banner_relatorio_mega.png", x=0, y=0, w=210)
        pdf.ln(25)
    except:
        pdf.ln(10)
    
    pdf.set_font(font_family, style="B", size=20)
    pdf.set_text_color(86, 8, 168)
    pdf.cell(0, 10, "Ata de Reunião Inteligente", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font(font_family, size=12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "Processado com Inteligência Artificial pela Mega Jr.", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(15)
    
    pdf.set_font(font_family, style="B", size=14)
    pdf.set_text_color(86, 8, 168)
    pdf.cell(0, 10, "INFORMAÇÕES DA REUNIÃO", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font(font_family, style="B", size=11)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(40, 7, "Data e Horário:")
    pdf.set_font(font_family, size=11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 7, dados.data_hora, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    pdf.set_font(font_family, style="B", size=14)
    pdf.set_text_color(86, 8, 168)
    pdf.cell(0, 10, "ANÁLISE E RESUMO EXECUTIVO (IA)", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font(font_family, size=11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 7, texto_processado) 

    pdf_bytes = bytes(pdf.output())
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Ata_Oficial_MegaJr.pdf"}
    )