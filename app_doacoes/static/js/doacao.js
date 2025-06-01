function limitTextLength(){
  const description = document.getElementsByClassName("card-text");
  for (let i = 0; i < description.length; i++) {
    if (description[i].innerHTML.length <= 90) continue;
    description[i].innerHTML = description[i].innerHTML.substring(0, 90) + "..."
  }
}

// Função para configurar cada carrossel com suporte touch
function setupCarousel(carouselId) {
  const container = document.getElementById(`carousel-${carouselId}`);
  const prevBtn = document.querySelector(
    `.carousel-prev[data-carousel="${carouselId}"]`
  );
  const nextBtn = document.querySelector(
    `.carousel-next[data-carousel="${carouselId}"]`
  );

  if (!container || !prevBtn || !nextBtn) return;

  const scrollAmount = () => {
    const card = container.querySelector(".card");
    return card ? (card.offsetWidth + 12) * 3 : 600;
  };

  // Navegação por botões
  prevBtn.onclick = (e) => {
    e.stopPropagation();
    container.scrollBy({ left: -scrollAmount(), behavior: "smooth" });
  };

  nextBtn.onclick = (e) => {
    e.stopPropagation();
    container.scrollBy({ left: scrollAmount(), behavior: "smooth" });
  };

  // SUPORTE TOUCH PARA MOBILE
  let startX = 0;
  let startY = 0;
  let scrollLeft = 0;
  let isDown = false;
  let hasMoved = false;

  // Touch Start (início do toque)
  container.addEventListener('touchstart', (e) => {
    isDown = true;
    hasMoved = false;
    startX = e.touches[0].pageX;
    startY = e.touches[0].pageY;
    scrollLeft = container.scrollLeft;
    container.style.cursor = 'grabbing';
  }, { passive: true });

  // Touch Move (arrastar)
  container.addEventListener('touchmove', (e) => {
    if (!isDown) return;
    
    const x = e.touches[0].pageX;
    const y = e.touches[0].pageY;
    const walkX = (x - startX) * 2; // Multiplicador para sensibilidade
    const walkY = Math.abs(y - startY);
    
    // Se o movimento horizontal for maior que vertical, previne scroll vertical
    if (Math.abs(walkX) > walkY) {
      e.preventDefault();
      hasMoved = true;
      container.scrollLeft = scrollLeft - walkX;
    }
  }, { passive: false });

  // Touch End (fim do toque)
  container.addEventListener('touchend', () => {
    isDown = false;
    container.style.cursor = 'grab';
  }, { passive: true });

  // SUPORTE MOUSE PARA DESKTOP (opcional, melhora UX)
  container.addEventListener('mousedown', (e) => {
    isDown = true;
    hasMoved = false;
    startX = e.pageX - container.offsetLeft;
    scrollLeft = container.scrollLeft;
    container.style.cursor = 'grabbing';
  });

  container.addEventListener('mouseleave', () => {
    isDown = false;
    container.style.cursor = 'grab';
  });

  container.addEventListener('mouseup', () => {
    isDown = false;
    container.style.cursor = 'grab';
  });

  container.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    hasMoved = true;
    const x = e.pageX - container.offsetLeft;
    const walk = (x - startX) * 2;
    container.scrollLeft = scrollLeft - walk;
  });

  // Previne cliques acidentais após arrastar
  container.addEventListener('click', (e) => {
    if (hasMoved) {
      e.preventDefault();
      e.stopPropagation();
    }
  });

  // Estilo inicial do cursor
  container.style.cursor = 'grab';
}

// Configura todos os carrosseis
document.addEventListener("DOMContentLoaded", () => {
  ["urgente", "sugestoes", "explorar"].forEach(setupCarousel);

  // Efeitos de hover (apenas para desktop)
  if (!('ontouchstart' in window)) {
    document.querySelectorAll(".card").forEach((card) => {
      card.onmouseenter = () => {
        card.style.transform = "scale(1.05)";
      };

      card.onmouseleave = () => {
        card.style.transform = "scale(1)";
      };
    });
  }


  limitTextLength();
});

document.getElementById('filtroCategoria').addEventListener('change', function () {
  const categoria = this.value;

  fetch(`/doacoes?categoria=${categoria}`, {
    headers: {
      'X-Requested-With': 'XMLHttpRequest' 
    }
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById('carousel-explorar').innerHTML = data.html;
      limitTextLength();
    });
});