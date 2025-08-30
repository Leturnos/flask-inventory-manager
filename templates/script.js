function Adicionado(){
    window.alert("Item adicionado com sucesso")
}

function BuscarDados() {
  fetch('/dados')
    .then(response => response.json())
    .then(data => {
      const nome = data.nome;
      const valor = data.valor;

      document.getElementById("results").innerText = `Item: ${nome}, Valor: R$ ${valor.toFixed(2)}`;
    })
    .catch(error => {
      console.error('Erro ao buscar dados:', error);
    })
};

      