 // Função para configurar cada carrossel
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

    prevBtn.onclick = (e) => {
      e.stopPropagation();
      container.scrollBy({ left: -scrollAmount(), behavior: "smooth" });
    };

    nextBtn.onclick = (e) => {
      e.stopPropagation();
      container.scrollBy({ left: scrollAmount(), behavior: "smooth" });
    };
  }

  // Configura todos os carrosseis
  document.addEventListener("DOMContentLoaded", () => {
    ["urgente", "sugestoes", "explorar"].forEach(setupCarousel);

    // Efeitos de hover
    document.querySelectorAll(".card").forEach((card) => {
      card.onmouseenter = () => {
        card.style.transform = "scale(1.05)";
      };

      card.onmouseleave = () => {
        card.style.transform = "scale(1)";
      };
    });
  });