function limitTextLength(){
  const description = document.getElementsByClassName("card-text");
  for (let i = 0; i < description.length; i++) {
    if (description[i].innerHTML.length <= 90) continue;
    description[i].innerHTML = description[i].innerHTML.substring(0, 90) + "..."
  }
}

document.addEventListener('DOMContentLoaded', function() {
  limitTextLength();
});

document.getElementById('filtroCategoria').addEventListener('change', function() {
    const categoriaSelecionada = this.value;
    const ongs = document.querySelectorAll('.ong-item'); // Adicione esta classe aos cards das ONGs
    
    ongs.forEach(function(ong) {
        if (categoriaSelecionada === 'todas') {
            ong.style.display = 'block';
        } else {
            // Assumindo que você tem um atributo data-categoria no elemento da ONG
            const categoriaOng = ong.getAttribute('data-categoria');
            if (categoriaOng && categoriaOng.toLowerCase().includes(categoriaSelecionada.toLowerCase())) {
                ong.style.display = 'block';
            } else {
                ong.style.display = 'none';
            }
        }
    });
});



