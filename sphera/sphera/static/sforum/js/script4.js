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




//const sliderWrapper = document.querySelector('.slider-wrapper');
//const prevButton = document.querySelector('.slider-button-prev');
//const nextButton = document.querySelector('.slider-button-next');
//let cardWidth = document.querySelector('.card1').offsetWidth + 20; // Ширина карточки + margin
//let currentPosition = 0;
//let numCardsVisible = 5;
//
//function updateVisibleCards() {
//  const containerWidth = document.querySelector('.slider-container').offsetWidth;
//  if (containerWidth < 480) {
//    numCardsVisible = 1.33; // 1 карточка + половина следующей
//  } else if (containerWidth < 786) {
//    numCardsVisible = 2;
//  } else {
//    numCardsVisible = 5;
//  }
//}
//
//updateVisibleCards();
//
//function slide(direction) {
//  const maxPosition = -(cardWidth * (sliderWrapper.children.length - numCardsVisible));
//
//  if (direction === 'next') {
//    currentPosition -= cardWidth;
//  } else if (direction === 'prev') {
//    currentPosition += cardWidth;
//  }
//
//  if (currentPosition < maxPosition) {
//    currentPosition = maxPosition;
//  }
//  if (currentPosition > 0) {
//    currentPosition = 0;
//  }
//
//  sliderWrapper.style.transform = `translateX(${currentPosition}px)`;
//}
//
//if (prevButton && nextButton) {
//  nextButton.addEventListener('click', () => slide('next'));
//  prevButton.addEventListener('click', () => slide('prev'));
//}
//
//window.addEventListener('resize', () => {
//  currentPosition = 0;
//  sliderWrapper.style.transform = `translateX(0px)`;
//  cardWidth = document.querySelector('.card1').offsetWidth + 20;
//  updateVisibleCards();
//});
//
//// Поддержка свайпа
//let touchStartX = 0;
//let touchEndX = 0;
//
//sliderWrapper.addEventListener('touchstart', (e) => {
//  touchStartX = e.touches[0].clientX;
//});
//
//sliderWrapper.addEventListener('touchmove', (e) => {
//  touchEndX = e.touches[0].clientX;
//});
//
//sliderWrapper.addEventListener('touchend', () => {
//  if (touchStartX - touchEndX > 50) {
//    // Свайп вправо (следующая карточка)
//    slide('next');
//  } else if (touchEndX - touchStartX > 50) {
//    // Свайп влево (предыдущая карточка)
//    slide('prev');
//  }
//});
const sliderWrapper = document.querySelector('.slider-wrapper');
const prevButton = document.querySelector('.slider-button-prev');
const nextButton = document.querySelector('.slider-button-next');
const cards = document.querySelectorAll('.card1');
const totalCards = cards.length;
let cardWidth = cards[0].offsetWidth + 20;
let currentIndex = 0;
let isDragging = false;
let startX = 0;
let currentTranslate = 0;
let prevTranslate = 0;
let animationID;

function updateCardWidth() {
  cardWidth = cards[0].offsetWidth + 20;
}

function setSliderPosition() {
  sliderWrapper.style.transform = `translateX(${currentTranslate}px)`;
}

function moveSlide(direction) {
  currentIndex += direction;
  if (currentIndex < 0) {
    currentIndex = totalCards - 1;
  } else if (currentIndex >= totalCards) {
    currentIndex = 0;
  }
  currentTranslate = -currentIndex * cardWidth;
  setSliderPosition();
}

function touchStart(event) {
  isDragging = true;
  startX = event.touches ? event.touches[0].clientX : event.clientX;
  prevTranslate = currentTranslate;
  animationID = requestAnimationFrame(setSliderPosition);
}

function touchMove(event) {
  if (!isDragging) return;
  const currentX = event.touches ? event.touches[0].clientX : event.clientX;
  const diff = currentX - startX;
  currentTranslate = prevTranslate + diff;
}

function touchEnd() {
  isDragging = false;
  cancelAnimationFrame(animationID);
  const movedBy = currentTranslate - prevTranslate;
  if (movedBy < -50) moveSlide(1);
  else if (movedBy > 50) moveSlide(-1);
  else currentTranslate = prevTranslate;
  setSliderPosition();
}

if (prevButton && nextButton) {
  nextButton.addEventListener('click', () => moveSlide(1));
  prevButton.addEventListener('click', () => moveSlide(-1));
}

sliderWrapper.addEventListener('mousedown', touchStart);
sliderWrapper.addEventListener('mousemove', touchMove);
sliderWrapper.addEventListener('mouseup', touchEnd);
sliderWrapper.addEventListener('mouseleave', touchEnd);
sliderWrapper.addEventListener('touchstart', touchStart);
sliderWrapper.addEventListener('touchmove', touchMove);
sliderWrapper.addEventListener('touchend', touchEnd);

window.addEventListener('resize', updateCardWidth);

// Инициализация позиции слайдера
setSliderPosition();