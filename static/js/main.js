document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const filter = searchInput.value.toLowerCase();
            document.querySelectorAll('.phone-card').forEach(card => {
                card.style.display = card.textContent.toLowerCase().includes(filter) ? '' : 'none';
            });
        });
    }
}); 