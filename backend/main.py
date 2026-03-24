import os
from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fpdf import FPDF
from dotenv import load_dotenv
from google import genai

# 1. Carrega as senhas do arquivo .env
load_dotenv()

# 2. Configura o cliente do Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# INICIALIZAÇÃO DA API (Mova isso para o topo!)

app = FastAPI()

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

# DEFINIÇÃO DO PADRÃO DO PDF (Design Mega)
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
        
        self.set_fill_color(255, 222, 89) # Amarelo Mega
        self.rect(0, 290, 210, 7, style="F")
        
        self.set_y(-7)
        try:
            self.set_font("Montserrat", "B", 8)
        except:
            self.set_font("helvetica", "B", 8)
            
        self.set_text_color(0, 0, 0)
        self.cell(0, 5, f'Página {self.page_no()}/{{nb}}', align='C')



# ROTA PRINCIPAL: GERAR PDF

@app.post("/api/gerar-pdf")
def gerar_pdf(dados: DadosAta):
    
    # O CÉREBRO DA OPERAÇÃO: CHAMANDO O GEMINI
    
    instrucao = f"""
    Você é um assistente executivo sênior da Mega Jr.
    
    ⚠️ REGRA DE SEGURANÇA MÁXIMA:
    Avalie o texto fornecido pelo usuário. Se ele for apenas letras aleatórias sem sentido (ex: "asdasdasd", "kjdfhgk"), xingamentos, ou não contiver absolutamente nenhuma informação real de uma reunião, você DEVE abortar a missão e responder EXATAMENTE e APENAS com a palavra: ERRO_TEXTO_INVALIDO. Não explique o motivo, apenas devolva essa palavra.
    
    Anotações cruas:
    - Detalhes: {dados.detalhes}
    - Pontos Soltos: {dados.pontos_importantes}
    
    Se o texto for minimamente válido, crie um texto estruturado da seguinte forma:
    RESUMO EXECUTIVO:
    (Escreva 1 ou 2 parágrafos formais resumindo a reunião).
    
    AÇÕES DEFINIDAS:
    (Liste os próximos passos usando hífens - como bullet points).
    
    Não use formatação Markdown (como ** ou #), apenas texto limpo.
    """
    
    resposta_ia = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=instrucao,
    )
    texto_processado = resposta_ia.text.strip()
    
    # Interceptador de Erros do texto aleatório
    if texto_processado == "ERRO_TEXTO_INVALIDO":
        raise HTTPException(
            status_code=400, 
            detail="O texto inserido não faz sentido. Por favor, escreva anotações reais da reunião! 🦆"
        )
        
   
    # GERANDO O PDF COM AS LINHAS ROXAS
   
    pdf = MegaJrPDF()
    pdf.alias_nb_pages()

    using_montserrat = pdf.load_custom_fonts()
    font_family = "Montserrat" if using_montserrat else "helvetica"

    pdf.add_page()
    
    # Banner Topo
    try:
        pdf.image("assets/banner_relatorio_mega.png", x=0, y=0, w=210)
        pdf.ln(25)
    except:
        pdf.ln(10)
    
    # Cabeçalho Principal
    pdf.set_font(font_family, style="B", size=18)
    pdf.set_text_color(50, 50, 50)
    
    # IMPORTANTE: Encode 'latin-1' para evitar erros de acentuação no FPDF
    titulo = "ATA DE REUNIÃO INTELIGENTE".encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 18, titulo, new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font(font_family, size=11)
    pdf.set_text_color(100, 100, 100)
    subtitulo = "Processado com Inteligência Artificial pela Mega Jr.".encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 18, subtitulo, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    
    # --- Seção 1: Informações Básicas ---
    pdf.set_font(font_family, style="B", size=12)
    pdf.set_text_color(86, 8, 168) # Roxo Mega
    
    sec1 = "INFORMAÇÕES DA REUNIÃO".encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 8, sec1, new_x="LMARGIN", new_y="NEXT")
    
    # LINHA ROXA 1
    pdf.set_fill_color(86, 8, 168)
    pdf.rect(15, pdf.get_y(), 180, 0.5, style="F") 
    pdf.ln(3)
    
    pdf.set_font(font_family, style="B", size=11)
    pdf.set_text_color(30, 30, 30)
    label_data = "Data e Horário:".encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(35, 7, label_data)
    
    pdf.set_font(font_family, size=11)
    pdf.set_text_color(50, 50, 50)
    
    data_limpa = dados.data_hora.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 7, data_limpa, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # --- Seção 2: O Resumo Inteligente (IA) ---
    pdf.set_font(font_family, style="B", size=12)
    pdf.set_text_color(86, 8, 168) # Roxo Mega
    
    sec2 = "ANÁLISE E RESUMO EXECUTIVO (IA)".encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 8, sec2, new_x="LMARGIN", new_y="NEXT")
    
    # LINHA ROXA 2
    pdf.set_fill_color(86, 8, 168)
    pdf.rect(15, pdf.get_y(), 180, 0.5, style="F")
    pdf.ln(3)
    
    pdf.set_font(font_family, size=11)
    pdf.set_text_color(50, 50, 50)
    
    # Corrige os caracteres do texto gigantesco que volta do Gemini
    texto_final = texto_processado.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, texto_final) 

    pdf_bytes = bytes(pdf.output())
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Ata_Oficial_MegaJr.pdf"}
    )