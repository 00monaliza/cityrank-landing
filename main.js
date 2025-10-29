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
  document.getElementById("registerModal").style.display = "flex";
}

function closeModal() {
  document.getElementById("registerModal").style.display = "none";
}

function submitRegistration() {
  const name = document.getElementById("userName").value.trim();
  const phone = document.getElementById("userPhone").value.trim();

  if (!name || !phone) {
    alert("Пожалуйста, введите имя и номер телефона.");
    return;
  }

  closeModal();
  window.location.href = "https://chat.whatsapp.com/KwPH71LaduF1tFXbquIXjc";
}

