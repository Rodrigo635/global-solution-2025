class GalleryManager {
    constructor() {
        this.maxFiles = 6;
        this.maxFileSize = 5 * 1024 * 1024; // 5MB
        this.allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        this.selectedFiles = [];
        
        this.initializeElements();
        this.setupEventListeners();
    }
    
    initializeElements() {
        this.uploadArea = document.getElementById('uploadArea');
        this.previewContainer = document.getElementById('galleryPreviewContainer');
        this.previewsDiv = document.getElementById('galleryPreviews');
        this.countDisplay = document.getElementById('galleryCount');
        
        // Encontrar o campo Django ou criar input manual
        this.fileInput = document.querySelector('input[name="gallery_images"]');
        if (!this.fileInput) {
            this.fileInput = document.createElement('input');
            this.fileInput.type = 'file';
            this.fileInput.name = 'gallery_images';
            this.fileInput.multiple = true;
            this.fileInput.accept = 'image/*';
            this.fileInput.style.display = 'none';
            this.uploadArea.appendChild(this.fileInput);
        }
        
        // Ocultar o input original
        this.fileInput.style.display = 'none';
    }
    
    setupEventListeners() {
        // Click para selecionar arquivos
        this.uploadArea.addEventListener('click', () => {
            this.fileInput.click();
        });
        
        // Seleção de arquivos
        this.fileInput.addEventListener('change', (e) => {
            this.handleFiles(Array.from(e.target.files));
        });
        
        // Drag and drop
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });
        
        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('dragover');
        });
        
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            this.handleFiles(Array.from(e.dataTransfer.files));
        });
    }
    
    handleFiles(files) {
        const validFiles = [];
        const errors = [];
        
        // Verificar se adicionar estes arquivos excederia o limite
        if (this.selectedFiles.length + files.length > this.maxFiles) {
            errors.push(`Máximo de ${this.maxFiles} imagens permitidas.`);
            return this.showErrors(errors);
        }
        
        files.forEach(file => {
            // Validar tipo de arquivo
            if (!this.allowedTypes.includes(file.type)) {
                errors.push(`${file.name}: Formato não suportado. Use JPG ou PNG.`);
                return;
            }
            
            // Validar tamanho do arquivo
            if (file.size > this.maxFileSize) {
                errors.push(`${file.name}: Arquivo muito grande. Máximo 5MB.`);
                return;
            }
            
            // Verificar duplicatas
            if (this.selectedFiles.some(f => f.name === file.name && f.size === file.size)) {
                errors.push(`${file.name}: Arquivo já selecionado.`);
                return;
            }
            
            validFiles.push(file);
        });
        
        if (errors.length > 0) {
            this.showErrors(errors);
            return;
        }
        
        // Adicionar arquivos válidos
        this.selectedFiles = [...this.selectedFiles, ...validFiles];
        this.updateFileInput();
        this.updatePreview();
    }
    
    removeFile(index) {
        this.selectedFiles.splice(index, 1);
        this.updateFileInput();
        this.updatePreview();
    }
    
    updateFileInput() {
        // Criar novo objeto FileList
        const dt = new DataTransfer();
        this.selectedFiles.forEach(file => dt.items.add(file));
        this.fileInput.files = dt.files;
    }
    
    updatePreview() {
        if (this.selectedFiles.length === 0) {
            this.previewContainer.style.display = 'none';
            return;
        }
        
        this.previewContainer.style.display = 'block';
        this.previewsDiv.innerHTML = '';
        
        this.selectedFiles.forEach((file, index) => {
            const col = document.createElement('div');
            col.className = 'col-6 col-sm-4 col-md-3 col-lg-2';
            
            const previewItem = document.createElement('div');
            previewItem.className = 'gallery-preview-item';
            
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            img.alt = file.name;
            img.style.width = '100%';
            img.style.height = '100%';
            img.style.objectFit = 'cover';
            
            const removeBtn = document.createElement('button');
            removeBtn.className = 'gallery-remove-btn';
            removeBtn.innerHTML = '×';
            removeBtn.type = 'button';
            removeBtn.onclick = () => this.removeFile(index);
            
            previewItem.appendChild(img);
            previewItem.appendChild(removeBtn);
            col.appendChild(previewItem);
            this.previewsDiv.appendChild(col);
        });
        
        this.countDisplay.textContent = `${this.selectedFiles.length}/${this.maxFiles} imagens selecionadas`;
    }
    
    showErrors(errors) {
        // Remover mensagens de erro existentes
        const existingErrors = document.querySelectorAll('.gallery-error-message');
        existingErrors.forEach(el => el.remove());
        
        // Adicionar novas mensagens de erro
        const errorDiv = document.createElement('div');
        errorDiv.className = 'gallery-error-message error-message mt-2';
        errors.forEach(error => {
            const errorP = document.createElement('div');
            errorP.textContent = error;
            errorDiv.appendChild(errorP);
        });
        
        this.uploadArea.parentNode.appendChild(errorDiv);
        
        // Remover erros após 5 segundos
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }
}

// Inicializar quando DOM carregar
document.addEventListener('DOMContentLoaded', () => {
    new GalleryManager();
});

// Validação do formulário antes do submit
document.getElementById('ongRegistrationForm').addEventListener('submit', function(e) {
    const fileInput = document.querySelector('input[name="gallery_images"]');
    const files = fileInput.files;
    
    if (files.length > 6) {
        e.preventDefault();
        alert('Máximo de 6 imagens permitidas.');
        return false;
    }
    
    for (let file of files) {
        if (file.size > 5 * 1024 * 1024) {
            e.preventDefault();
            alert(`A imagem ${file.name} excede o tamanho máximo de 5MB.`);
            return false;
        }
    }
});
