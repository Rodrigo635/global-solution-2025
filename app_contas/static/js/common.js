document.addEventListener('DOMContentLoaded', function () {
  const imageInput = document.getElementById('id_imagem');
  const imagePreview = document.getElementById('imagePreview');
  const imagePreviewContainer = document.getElementById('imagePreviewContainer');
  const removeImageBtn = document.getElementById('removeImage');

  // Verificar se já tem imagem ao carregar a página (para casos de erro no formulário)
  if (imageInput.files && imageInput.files[0]) {
    const reader = new FileReader();
    reader.onload = function (e) {
      imagePreview.src = e.target.result;
      imagePreviewContainer.style.display = 'block';
    };
    reader.readAsDataURL(imageInput.files[0]);
  }

  // Mostrar preview quando nova imagem é selecionada
  imageInput.addEventListener('change', function (e) {
    if (this.files && this.files[0]) {
      const reader = new FileReader();
      reader.onload = function (e) {
        imagePreview.src = e.target.result;
        imagePreviewContainer.style.display = 'block';
      };
      reader.readAsDataURL(this.files[0]);
    } else {
      imagePreviewContainer.style.display = 'none';
    }
  });

  // Remover imagem selecionada
  removeImageBtn.addEventListener('click', function () {
    imageInput.value = '';
    imagePreview.src = '';
    imagePreviewContainer.style.display = 'none';
  });
});

// Aguardar o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    const paisSelect = document.getElementById('id_pais');
    const estadoSelect = document.getElementById('id_estado');
    const cidadeSelect = document.getElementById('id_cidade');

    // Listener para quando o país for selecionado
    paisSelect.addEventListener('change', function() {
        const paisId = this.value;
        carregarEstados(paisId);
    });

    // Listener para quando o estado for selecionado
    estadoSelect.addEventListener('change', function() {
        const estadoId = this.value;
        carregarCidades(estadoId);
    });

    // Função para carregar estados
    function carregarEstados(paisId) {
        // Limpar opções atuais
        estadoSelect.innerHTML = '<option value="">Selecione um estado</option>';
        cidadeSelect.innerHTML = '<option value="">Selecione uma cidade</option>';
        
        if (paisId) {
            // Fazer requisição AJAX
            fetch(`/contas/carregar-estados/?pais_id=${paisId}`)
                .then((response) => response.json())
                .then((data) => {
                    data.estados.forEach((estado) => {
                        const option = document.createElement('option');
                        option.value = estado.id;
                        option.textContent = estado.nome;
                        estadoSelect.appendChild(option);
                    });
                })
                .catch((error) => {
                    console.error('Erro ao carregar estados:', error);
                });
        }
    }

    // Função para carregar cidades
    function carregarCidades(estadoId) {
        // Limpar opções atuais
        cidadeSelect.innerHTML = '<option value="">Selecione uma cidade</option>';
        
        if (estadoId) {
            // Fazer requisição AJAX
            fetch(`/contas/carregar-cidades/?estado_id=${estadoId}`)
                .then((response) => response.json())
                .then((data) => {
                    data.cidades.forEach((cidade) => {
                        const option = document.createElement('option');
                        option.value = cidade.id;
                        option.textContent = cidade.nome;
                        cidadeSelect.appendChild(option);
                    });
                })
                .catch((error) => {
                    console.error('Erro ao carregar cidades:', error);
                });
        }
    }
});
