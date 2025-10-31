document.addEventListener('DOMContentLoaded', function() {
    const courseCards = document.querySelectorAll('.course-card');
    
    courseCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    const submoduleLinks = document.querySelectorAll('.submodule-link');
    submoduleLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const span = this.querySelector('span');
            span.textContent = 'Launching...';
        });
    });
});
