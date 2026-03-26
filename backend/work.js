// ==========================================
// 1. EFEITO DIGITAÇÃO (TYPEWRITER)
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
  const titulo = document.querySelector(".Ata-Reuniao ")
  if (titulo) {
    const texto = titulo.innerHTML
    titulo.innerHTML = ""
    let index = 0
    function digitar() {
      if (index < texto.length) {
        titulo.innerHTML += texto.charAt(index)
        index++
        setTimeout(digitar, 100)
      }
    }
    setTimeout(digitar, 500)
  }
})

// ==========================================
// 2. INTEGRAÇÃO COM IA E ANIMAÇÕES
// ==========================================

const btnGerar = document.querySelector(".btn-amarelo")
const txtData = document.querySelector(".caixa-data-hora")
const txtDetalhes = document.querySelector(
  'textarea[placeholder="Coloque os detalhes da ata"]',
)
const txtPontos = document.querySelector(
  'textarea[placeholder="Coloque os pontos mais importantes"]',
)

const conversorSection = document.getElementById("conversor")
const resultadoContainer = document.getElementById("resultado-container")
const btnBaixarLower = document.getElementById("btn-baixar")

let pdfBlobGerado = null // Guardará o PDF aqui

btnGerar.addEventListener("click", async () => {
  // Validação inicial
  if (!txtData.value || !txtPontos.value) {
    alert("Preencha todos os campos primeiro! 🦆")
    return
  }

  // Início: Muda o botão e rola a tela
  btnGerar.innerText = "IA pensando... ✨"
  btnGerar.disabled = true
  conversorSection.scrollIntoView({ behavior: "smooth" })

  // Mostra o Patinho (Ajuste o caminho da imagem se necessário)
  resultadoContainer.innerHTML = `
      <style>
          /* 1. Mágica do Círculo Perfeito: Dimensões iguais + border-radius 50% */
          .pato-circular {
              width: 100px;
              height: 100px; /* Precisa ser igual à width */
              border-radius: 50%; /* Faz o círculo */
              object-fit: cover; /* Garante que o GIF preencha sem distorcer */
              border: 3px solid #ffde59; /* Opcional: Bordinha Amarela Mega */
              box-shadow: 0 4px 15px rgba(255, 222, 89, 0.3); /* Opcional: Glow sutil */
              
              /* Mantemos a animação de órbita que você já amou */
              position: absolute;
              animation: orbitar 3s linear infinite;
              z-index: 20;
          }

          /* Mágica da Órbita: O patinho gira 360º, se afasta do centro (translateX), e desfaz o giro (rotate(-360deg)) */
          @keyframes orbitar {
              0% { transform: rotate(0deg) translateX(125px) rotate(0deg); }
              100% { transform: rotate(360deg) translateX(125px) rotate(-360deg); }
          }
      </style>
      
      <div style="display: flex; align-items: center; justify-content: center; height: 280px; position: relative;">
          
          <p style="color: white; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 16px; position: absolute; text-align: center; z-index: 10; margin: 0; line-height: 1.4;">
              O patinho está<br>
              <span style="color: #ffde59; font-weight: bold;">organizando a ata...</span>
          </p>
          
          <img src="assets/patinho.gif" alt="Carregando..." class="pato-circular">
          
      </div>
  `
  btnBaixarLower.style.display = "none"

  try {
    const resposta = await fetch(
      "https://gerador-de-relatorios-i9im.onrender.com/api/gerar-pdf",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          data_hora: txtData.value,
          detalhes: txtDetalhes.value,
          pontos_importantes: txtPontos.value,
        }),
      },
    )

    // C) TRATAMENTO DE ERRO (Texto aleatório/inválido)
    if (!resposta.ok) {
      const erroData = await resposta.json()
      // Joga o erro para o bloco 'catch' lá embaixo
      throw new Error(erroData.detail || "Erro ao processar")
    }
    pdfBlobGerado = await resposta.blob()

    // ==========================================
    // A MÁGICA DA TRANSIÇÃO DE TELA
    // ==========================================

    // 1. MÁGICA DO FUNDO: Pegamos a caixa inteira e "limpamos" as listras roxas
    const caixaEsquerda = document.querySelector(".converter-left")
    caixaEsquerda.style.backgroundImage = "url('assets/ata_pronta.png')"
    caixaEsquerda.style.backgroundColor = "#111827" // Coloca um fundo escuro limpo
    caixaEsquerda.style.display = "flex" // Centraliza tudo
    caixaEsquerda.style.flexDirection = "column"
    caixaEsquerda.style.justifyContent = "center"
    caixaEsquerda.style.alignItems = "center"

    // 2. MÁGICA DO CONTEÚDO: Colocamos o texto de sucesso
    resultadoContainer.innerHTML = `
    <div style="text-align: center; animation: fadeIn 0.8s ease-in-out;">
        
        <h3 style="color: #000000; margin-top: 10px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 26px; font-weight: bold;">
            Ata Finalizada!
        </h3>
        <p style="color: #5608A8; margin-top: 8px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; max-width: 90%; margin: 10px auto;">
            O documento foi gerado e formatado nos padrões oficiais da Mega Jr.
        </p>
    </div>
    <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
`

    // Revela o botão
    btnBaixarLower.style.display = "flex"
  } catch (erro) {
    // Mostra a mensagem de erro (ex: "Texto sem sentido") na tela
    resultadoContainer.innerHTML = `
            <div style="text-align: center;">
                <h3 style="color: #ff5959; font-family: 'Plus Jakarta Sans';">Algo deu errado!</h3>
                <p style="color: white; margin-top: 10px;">${erro.message}</p>
            </div>
        `
  } finally {
    btnGerar.innerText = "Gerar Resumo"
    btnGerar.disabled = false
  }
})

// ==========================================
// 3. LÓGICA DO BOTÃO DE BAIXAR (FINAL)
// ==========================================
btnBaixarLower.addEventListener("click", () => {
  if (!pdfBlobGerado) return
  const url = window.URL.createObjectURL(pdfBlobGerado)
  const a = document.createElement("a")
  a.href = url
  a.download = "Ata_Oficial_MegaJr.pdf"
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
})
