// Функция для кнопки "ПРИНЯТЬ УЧАСТИЕ БЕСПЛАТНО"
function scrollToCTA() {
  document.getElementById("registerModal").style.display = "flex";
  
  // Отслеживаем клик на кнопку CTA
  if (typeof fbq !== 'undefined') {
    fbq('track', 'Lead');
  }
}

// Функция для кнопки "ЗАБРАТЬ БОНУСЫ И ЗАРЕГИСТРИРОВАТЬСЯ"
function registerRedirect() {
  document.getElementById("registerModal").style.display = "flex";
  
  // Отслеживаем открытие формы регистрации
  if (typeof fbq !== 'undefined') {
    fbq('track', 'Lead');
  }
}

// Закрытие модального окна
function closeModal() {
  document.getElementById("registerModal").style.display = "none";
}

// Отправка формы регистрации
function submitRegistration() {
  const name = document.getElementById("userName").value.trim();
  const phone = document.getElementById("userPhone").value.trim();

  if (!name || !phone) {
    alert("Пожалуйста, введите имя и номер телефона.");
    return;
  }

  // Отслеживаем успешную регистрацию
  if (typeof fbq !== 'undefined') {
    fbq('track', 'CompleteRegistration');
  }

  closeModal();
  window.location.href = "https://chat.whatsapp.com/KwPH71LaduF1tFXbquIXjc";
}

// Smooth scroll reveal animation для карточек
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
});

// Применяем анимацию ко всем карточкам
document.querySelectorAll('.program-card, .audience-card, .result-card, .success-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(30px)';
  el.style.transition = 'all 0.6s ease';
  observer.observe(el);
});