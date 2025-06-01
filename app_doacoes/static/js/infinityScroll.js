function limitTextLength(){
  const description = document.getElementsByClassName("card-text");
  for (let i = 0; i < description.length; i++) {
    if (description[i].innerHTML.length <= 90) continue;
    description[i].innerHTML = description[i].innerHTML.substring(0, 90) + "..."
  }
}

// Scroll Infinito para ONGs
class InfiniteScroll {
    constructor() {
        this.currentPage = 1;
        this.isLoading = false;
        this.hasNext = true;
        this.container = document.getElementById('ongs-container');
        this.loadingIndicator = document.getElementById('loading-indicator');
        
        this.init();
    }

    init() {
        // Criar indicador de loading se não existir
        if (!this.loadingIndicator) {
            this.createLoadingIndicator();
        }

        // Adicionar event listener para scroll
        window.addEventListener('scroll', this.handleScroll.bind(this));
        
        // Verificar se há dados iniciais sobre paginação
        this.checkInitialPagination();
    }

    createLoadingIndicator() {
        const loadingHTML = `
            <div id="loading-indicator" class="text-center py-4" style="display: none;">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Carregando mais ONGs...</span>
                </div>
                <p class="mt-2 text-muted">Carregando mais ONGs...</p>
            </div>
        `;
        
        this.container.insertAdjacentHTML('afterend', loadingHTML);
        this.loadingIndicator = document.getElementById('loading-indicator');
    }

    checkInitialPagination() {
        // Pegar informações da paginação inicial do template
        const paginationData = window.paginationData;
        if (paginationData) {
            this.hasNext = paginationData.hasNext;
            this.currentPage = paginationData.currentPage;
        }
    }

    handleScroll() {
        // Verificar se chegou perto do final da página
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        
        // Carregar quando estiver a 200px do final
        const threshold = 200;
        
        if (scrollTop + windowHeight >= documentHeight - threshold) {
            this.loadMore();
        }
    }

    async loadMore() {
        // Evitar múltiplas requisições simultâneas
        if (this.isLoading || !this.hasNext) {
            return;
        }

        this.isLoading = true;
        this.showLoading();

        try {
            const nextPage = this.currentPage + 1;
            const url = this.buildURL(nextPage);
            
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Adicionar novos cards ao container
            this.container.insertAdjacentHTML('beforeend', data.html);
            
            // Atualizar estado
            this.currentPage = nextPage;
            this.hasNext = data.has_next;
            
            // Executar script dos novos cards se necessário
            this.executeNewScripts();
            
        } catch (error) {
            console.error('Erro ao carregar mais ONGs:', error);
            this.showError();
        } finally {
            this.isLoading = false;
            this.hideLoading();
        }
        limitTextLength();
    }

    buildURL(page) {
        const url = new URL(window.location);
        url.searchParams.set('page', page);
        return url.toString();
    }

    executeNewScripts() {
        // Se houver scripts específicos para os novos cards, execute aqui
        // Exemplo: reinicializar tooltips, modals, etc.
        
        // Bootstrap tooltips
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => {
            if (!tooltip._tooltip) {
                new bootstrap.Tooltip(tooltip);
            }
        });
    }

    showLoading() {
        if (this.loadingIndicator) {
            this.loadingIndicator.style.display = 'block';
        }
    }

    hideLoading() {
        if (this.loadingIndicator) {
            this.loadingIndicator.style.display = 'none';
        }
    }

    showError() {
        // Mostrar mensagem de erro temporária
        const errorHTML = `
            <div class="alert alert-warning alert-dismissible fade show mt-3" role="alert">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Erro ao carregar mais ONGs. Tente novamente.
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        this.container.insertAdjacentHTML('afterend', errorHTML);
        
        // Remover erro após 5 segundos
        setTimeout(() => {
            const errorAlert = document.querySelector('.alert-warning');
            if (errorAlert) {
                errorAlert.remove();
            }
        }, 5000);
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    new InfiniteScroll();
});

// Também funcionar com Turbo/HTMX se estiver usando
document.addEventListener('turbo:load', function() {
    new InfiniteScroll();
});