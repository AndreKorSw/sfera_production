//const sliderWrapper = document.querySelector('.slider-wrapper');
//    const prevButton = document.querySelector('.slider-button-prev');
//    const nextButton = document.querySelector('.slider-button-next');
//    let cardWidth = document.querySelector('.card1').offsetWidth + 20; // Ширина карточки + margin
//    let currentPosition = 0;
//    let numCardsVisible = 5;
//
//    function updateVisibleCards() {
//      const containerWidth = document.querySelector('.slider-container').offsetWidth;
//      if (containerWidth < 480) {
//        numCardsVisible = 1.33; // 1 карточка + половина следующей
//      } else if (containerWidth < 786) {
//        numCardsVisible = 2;
//      } else {
//        numCardsVisible = 5;
//      }
//    }
//
//    updateVisibleCards();
//
//    function slide(direction) {
//      const maxPosition = -(cardWidth * (sliderWrapper.children.length - numCardsVisible));
//
//      if (direction === 'next') {
//        currentPosition -= cardWidth;
//      } else if (direction === 'prev') {
//        currentPosition += cardWidth;
//      }
//
//      if (currentPosition < maxPosition) {
//        currentPosition = maxPosition;
//      }
//      if (currentPosition > 0) {
//        currentPosition = 0;
//      }
//
//      sliderWrapper.style.transform = `translateX(${currentPosition}px)`;
//    }
//
//    if (prevButton && nextButton) {
//      nextButton.addEventListener('click', () => slide('next'));
//      prevButton.addEventListener('click', () => slide('prev'));
//    }
//
//    window.addEventListener('resize', () => {
//      currentPosition = 0;
//      sliderWrapper.style.transform = `translateX(0px)`;
//      cardWidth = document.querySelector('.card1').offsetWidth + 20;
//      updateVisibleCards();
//    });
const sliderWrapper = document.querySelector('.slider-wrapper');
const prevButtonSlider = document.querySelector('.slider-button-prev');
const nextButtonSlider = document.querySelector('.slider-button-next');
const cards = document.querySelectorAll('.card1');
const totalCards = cards.length;
let cardWidth = cards[0].offsetWidth + 20;
let currentIndexSlider = 0;
let isDraggingSlider = false;
let startXSlider = 0;
let currentTranslateSlider = 0;
let prevTranslateSlider = 0;
let animationIDSlider;

function updateCardWidth() {
  cardWidth = cards[0].offsetWidth + 20;
}

function setSliderPosition() {
  sliderWrapper.style.transform = `translateX(${currentTranslateSlider}px)`;
}

function moveSlideSlider(direction) {
  currentIndexSlider += direction;
  if (currentIndexSlider < 0) {
    currentIndexSlider = totalCards - 1;
  } else if (currentIndexSlider >= totalCards) {
    currentIndexSlider = 0;
  }
  currentTranslateSlider = -currentIndexSlider * cardWidth;
  setSliderPosition();
}

function touchStartSlider(event) {
  isDraggingSlider = true;
  startXSlider = event.touches ? event.touches[0].clientX : event.clientX;
  prevTranslateSlider = currentTranslateSlider;
  animationIDSlider = requestAnimationFrame(setSliderPosition);
}

function touchMoveSlider(event) {
  if (!isDraggingSlider) return;
  const currentXSlider = event.touches ? event.touches[0].clientX : event.clientX;
  const diffSlider = currentXSlider - startXSlider;
  currentTranslateSlider = prevTranslateSlider + diffSlider;
}

function touchEndSlider() {
  isDraggingSlider = false;
  cancelAnimationFrame(animationIDSlider);
  const movedBySlider = currentTranslateSlider - prevTranslateSlider;
  if (movedBySlider < -50) moveSlideSlider(1);
  else if (movedBySlider > 50) moveSlideSlider(-1);
  else currentTranslateSlider = prevTranslateSlider;
  setSliderPosition();
}

if (prevButtonSlider && nextButtonSlider) {
  nextButtonSlider.addEventListener('click', () => moveSlideSlider(1));
  prevButtonSlider.addEventListener('click', () => moveSlideSlider(-1));
}

sliderWrapper.addEventListener('mousedown', touchStartSlider);
sliderWrapper.addEventListener('mousemove', touchMoveSlider);
sliderWrapper.addEventListener('mouseup', touchEndSlider);
sliderWrapper.addEventListener('mouseleave', touchEndSlider);
sliderWrapper.addEventListener('touchstart', touchStartSlider);
sliderWrapper.addEventListener('touchmove', touchMoveSlider);
sliderWrapper.addEventListener('touchend', touchEndSlider);

window.addEventListener('resize', updateCardWidth);

// Инициализация позиции слайдера
setSliderPosition();