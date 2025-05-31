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
