document.addEventListener("DOMContentLoaded", () => {
    const fadeElements = document.querySelectorAll('.fade-section');
    const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
        } else {
        entry.target.classList.remove('fade-in');
        }
    });
    }, { threshold: 0 });
    fadeElements.forEach(el => observer.observe(el));
});