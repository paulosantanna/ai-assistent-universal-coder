document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.carousel-container');
  const slides = document.querySelectorAll('.carousel-slide');
  const prevBtn = document.querySelector('.carousel-arrow.prev');
  const nextBtn = document.querySelector('.carousel-arrow.next');

  if (!slides.length) return;

  let currentSlide = 0;
  let timer = null;

  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === index);
    });
    currentSlide = index;
  }

  function nextSlide() {
    const newIndex = (currentSlide + 1) % slides.length;
    showSlide(newIndex);
  }

  function prevSlide() {
    const newIndex = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(newIndex);
  }

  function startAutoPlay() {
    stopAutoPlay();
    timer = setInterval(nextSlide, 5000);
  }

  function stopAutoPlay() {
    if (timer) clearInterval(timer);
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', (e) => {
      e.preventDefault();
      nextSlide();
      startAutoPlay();
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', (e) => {
      e.preventDefault();
      prevSlide();
      startAutoPlay();
    });
  }

  if (container) {
    container.addEventListener('mouseenter', stopAutoPlay);
    container.addEventListener('mouseleave', startAutoPlay);
  }

  // Start initial auto play
  startAutoPlay();
});
