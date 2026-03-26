<div align="center">
  <img src="fronted/assets/ata_pronta.png" alt="Demonstração do Gerador de Atas" width="700px" />
</div>

<br>

# 📄✨ Gerador de Atas Inteligente - Mega Jr.

Uma aplicação web full-stack que utiliza Inteligência Artificial para transformar anotações rápidas e informais de reuniões em Atas Executivas profissionais, estruturadas e formatadas automaticamente em PDF nos padrões da empresa.

## 🚀 Funcionalidades

- **Processamento de Linguagem Natural:** Integração com o Google Gemini 2.5 para interpretar e estruturar anotações soltas, extraindo o resumo executivo e os próximos passos.
- **Validação de Texto (Anti-Gibberish):** A IA é treinada para identificar e rejeitar textos sem sentido (ex: "asdasd"), solicitando dados reais do usuário.
- **Geração de PDF Dinâmica:** Criação de documentos PDF on-the-fly utilizando `fpdf2`, com injeção de fontes customizadas (Montserrat), cores da marca e cabeçalhos oficiais.
- **Interface Fluida e Animada:** Front-end construído com Vanilla JavaScript puro, apresentando efeito de digitação (Typewriter), feedback visual de carregamento (animação do patinho) e transições suaves de estado.
- **Arquitetura Desacoplada:** Front-end hospedado na Vercel consumindo uma API RESTful hospedada no Render.

## 🛠️ Tecnologias Utilizadas

**Front-end:**
- HTML5, CSS3
- JavaScript (Vanilla / ES6+)
- Hospedagem: (https://mega-jr-atas.vercel.app/)

**Back-end:**
- Python 3
- [FastAPI] (Construção da API REST)
- [FPDF2] (Geração do PDF)
- Google GenAI SDK (Integração com Gemini)
- Hospedagem: [Render](https://render.com/)

## ⚙️ Como rodar o projeto localmente

1. **Clone o reposi



### 🇺🇸 English Version (`README-en.md`)

```markdown
# 📄✨ Smart Meeting Minutes Generator - Mega Jr.

A full-stack web application that leverages Artificial Intelligence to transform raw, informal meeting notes into professional, structured Executive Meeting Minutes, automatically formatted and exported as a standardized PDF.

## 🚀 Features

- **Natural Language Processing:** Integrates with Google Gemini 2.5 to interpret and structure loose notes, automatically generating an executive summary and a list of actionable next steps.
- **Gibberish Detection:** The AI prompt is engineered to identify and reject nonsensical text inputs (e.g., random keyboard mashing), prompting the user for valid meeting data.
- **Dynamic PDF Generation:** On-the-fly PDF creation using `fpdf2`, featuring custom font injection (Montserrat), brand colors, and official headers/footers.
- **Fluid & Animated UI:** Front-end built with pure Vanilla JavaScript, featuring a typewriter effect, visual loading feedback (orbiting duck animation), and smooth state transitions.
- **Decoupled Architecture:** Front-end hosted on Vercel communicating seamlessly with a RESTful API hosted on Render.

## 🛠️ Tech Stack

**Front-end:**
- HTML5, CSS3
- JavaScript (Vanilla / ES6+)
- Deployment: https://mega-jr-atas.vercel.app/

**Back-end:**
- Python 3
- [FastAPI] (REST API framework)
- [FPDF2] (PDF Generation)
- Google GenAI SDK (Gemini Integration)

