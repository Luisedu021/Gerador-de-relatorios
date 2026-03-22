document.addEventListener("DOMContentLoaded", () => {
  // Seleciona o título
  const titulo = document.querySelector(".Ata-Reuniao h1")

  // Guarda o texto que você escreveu no HTML ("Ata de Reunião Inteligente")
  const texto = titulo.innerHTML

  // Limpa o H1 para começar o efeito vazio
  titulo.innerHTML = ""

  let index = 0
  const velocidade = 100 // Tempo entre cada letra em milissegundos (100ms = rápido, 200ms = mais lento)

  // Função que digita letra por letra
  function digitar() {
    if (index < texto.length) {
      titulo.innerHTML += texto.charAt(index)
      index++
      setTimeout(digitar, velocidade) // Chama a função de novo até terminar a frase
    }
  }

  // Dá um pequeno atraso de meio segundo antes de começar a digitar (opcional, mas fica legal)
  setTimeout(digitar, 500)
})
