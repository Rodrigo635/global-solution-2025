  // Quando a página carregar
  document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('.main-header');

    window.addEventListener('scroll', function() {
      // Se rolou mais de 50px (ajuste conforme necessidade)
      if (window.scrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  });

    // Scrollar para seção
    // do botão do hero para seção sobre
    document.addEventListener("DOMContentLoaded", function () {
        document.getElementById("btn-hero").addEventListener("click", function (event) {
            event.preventDefault();
            const sobreSection = document.getElementById("sobre");
            const headerHeight = document.querySelector('header').offsetHeight;

            window.scrollTo({
                top: sobreSection.offsetTop - headerHeight - 20,
                behavior: "smooth"
            });
        });
    });

    // do header sobre para seção de sobre
    document.addEventListener("DOMContentLoaded", function () {
        document.getElementById("btn-sobre").addEventListener("click", function (event) {
            event.preventDefault();
            const sobreSection = document.getElementById("sobre");
            const headerHeight = document.querySelector('header').offsetHeight;

            window.scrollTo({
                top: sobreSection.offsetTop - headerHeight - 20,
                behavior: "smooth"
            });
        });
    });

    // do header funções para seção de funções
    document.addEventListener("DOMContentLoaded", function () {
        document.getElementById("btn-funcoes").addEventListener("click", function (event) {
            event.preventDefault();
            const funcoesSection = document.getElementById("funcoes");
            const headerHeight = document.querySelector('header').offsetHeight;

            window.scrollTo({
                top: funcoesSection.offsetTop - headerHeight - 40,
                behavior: "smooth"
            });
        });
    });

    // do header equipe para seção de equipe
    document.addEventListener("DOMContentLoaded", function () {
        document.getElementById("btn-equipe").addEventListener("click", function (event) {
            event.preventDefault();
            const equipeSection = document.getElementById("equipe");
            const headerHeight = document.querySelector('header').offsetHeight;

            window.scrollTo({
                top: equipeSection.offsetTop - headerHeight - 40,
                behavior: "smooth"
            });
        });
    });

    // do header contato para seção de contato
    document.addEventListener("DOMContentLoaded", function () {
        document.getElementById("btn-contato").addEventListener("click", function (event) {
            event.preventDefault();
            const contatoSection = document.getElementById("contato");
            const headerHeight = document.querySelector('header').offsetHeight;

            window.scrollTo({
                top: contatoSection.offsetTop - headerHeight,
                behavior: "smooth"
            });
        });
    });

document.addEventListener('DOMContentLoaded', function () {
  const header = document.querySelector('.main-header');
  const navbarCollapse = document.getElementById('navbarSupportedContent');

  const toggleScrolledClass = () => {
    if (navbarCollapse.classList.contains('show')) {
      header.classList.add('scrolled');
    } else if (window.scrollY <= 50) {
      header.classList.remove('scrolled');
    }
  };

  // Escuta o evento de abertura/fechamento do menu
  navbarCollapse.addEventListener('shown.bs.collapse', toggleScrolledClass);
  navbarCollapse.addEventListener('hidden.bs.collapse', toggleScrolledClass);
});