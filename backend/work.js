// ==========================================
// 1. EFEITO DIGITAÇÃO (TYPEWRITER)
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
  const titulo = document.querySelector(".Ata-Reuniao h1")
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
  if (!txtData.value || !txtDetalhes.value || !txtPontos.value) {
    alert("Preencha todos os campos primeiro! 🦆")
    return
  }

  // A) Início: Muda o botão e rola a tela
  btnGerar.innerText = "IA pensando... ✨"
  btnGerar.disabled = true
  conversorSection.scrollIntoView({ behavior: "smooth" })

  // B) Mostra o Patinho (Ajuste o caminho da imagem se necessário)
  resultadoContainer.innerHTML = `
        <div style="text-align: center;">
            <img src="assets/patinho.gif" alt="Carregando..." style="width: 150px;">
            <p style="color:white; margin-top:10px; font-family: 'Plus Jakarta Sans';">O patinho está organizando a ata...</p>
        </div>
    `
  btnBaixarLower.style.display = "none"

  try {
    const resposta = await fetch("http://127.0.0.1:8000/api/gerar-pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        data_hora: txtData.value,
        detalhes: txtDetalhes.value,
        pontos_importantes: txtPontos.value,
      }),
    })

    // C) TRATAMENTO DE ERRO (Texto aleatório/inválido)
    if (!resposta.ok) {
      const erroData = await resposta.json()
      // Joga o erro para o bloco 'catch' lá embaixo
      throw new Error(erroData.detail || "Erro ao processar")
    }

    // D) SUCESSO: Recebe o PDF
    pdfBlobGerado = await resposta.blob()

    // Troca o patinho pela imagem de sucesso
    resultadoContainer.innerHTML = `
            <div style="text-align: center;">
                <img src="assets/pdf-pronto.png" alt="Sucesso" style="width: 100px;">
                <h3 style="color:#ffde59; margin-top:10px; font-family: 'Plus Jakarta Sans';">Ata Pronta!</h3>
            </div>
        `
    btnBaixarLower.style.display = "block"
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
