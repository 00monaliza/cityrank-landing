function scrollToCTA() {
    document.getElementById('cta').scrollIntoView({ behavior: 'smooth' });
}

// Smooth scroll reveal animation
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
});

document.querySelectorAll('.program-card, .audience-card, .result-card, .success-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'all 0.6s ease';
    observer.observe(el);
});

function registerRedirect() {
  if (confirm("Переход на форму регистрации в WhatsApp-группу. Продолжить?")) {
    window.location.href = "https://chat.whatsapp.com/KwPH71LaduF1tFXbquIXjc";
  }
}
