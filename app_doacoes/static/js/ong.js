document.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('.photos');
    let maxHeight = 0;
    items.forEach(item => {
      const height = item.offsetHeight;
      if (height > maxHeight) maxHeight = height;
    });
    items.forEach(item => item.style.height = maxHeight + 'px');


    const description = document.getElementById('description-text');
    const btnReadMore = document.getElementById('read-more');

    if (description && btnReadMore) {
        const fullText = description.innerText.trim();
        const words = fullText.split(/\s+/);

        if (words.length > 100) {
            const shortText = words.slice(0, 100).join(' ') + '...';
            let isExpanded = false;

            description.setAttribute('data-full', fullText);
            description.setAttribute('data-short', shortText);
            description.innerText = shortText;
            btnReadMore.style.display = 'inline';
            btnReadMore.textContent = 'Ver mais';

            btnReadMore.addEventListener('click', () => {
                if (isExpanded) {
                    description.innerText = description.getAttribute('data-short');
                    btnReadMore.textContent = 'Ver mais';
                } else {
                    description.innerText = description.getAttribute('data-full');
                    btnReadMore.textContent = 'Ver menos';
                }
                isExpanded = !isExpanded;
            });
        }
    }
});
