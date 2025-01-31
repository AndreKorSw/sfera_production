const sliderWrapper = document.querySelector('.slider-wrapper');
    const prevButton = document.querySelector('.slider-button-prev');
    const nextButton = document.querySelector('.slider-button-next');
    let cardWidth = document.querySelector('.card1').offsetWidth + 20; // Ширина карточки + margin
    let currentPosition = 0;
    let numCardsVisible = 5;

    function updateVisibleCards() {
      const containerWidth = document.querySelector('.slider-container').offsetWidth;
      if (containerWidth < 480) {
        numCardsVisible = 1.33; // 1 карточка + половина следующей
      } else if (containerWidth < 786) {
        numCardsVisible = 2;
      } else {
        numCardsVisible = 5;
      }
    }

    updateVisibleCards();

    function slide(direction) {
      const maxPosition = -(cardWidth * (sliderWrapper.children.length - numCardsVisible));

      if (direction === 'next') {
        currentPosition -= cardWidth;
      } else if (direction === 'prev') {
        currentPosition += cardWidth;
      }

      if (currentPosition < maxPosition) {
        currentPosition = maxPosition;
      }
      if (currentPosition > 0) {
        currentPosition = 0;
      }

      sliderWrapper.style.transform = `translateX(${currentPosition}px)`;
    }

    if (prevButton && nextButton) {
      nextButton.addEventListener('click', () => slide('next'));
      prevButton.addEventListener('click', () => slide('prev'));
    }

    window.addEventListener('resize', () => {
      currentPosition = 0;
      sliderWrapper.style.transform = `translateX(0px)`;
      cardWidth = document.querySelector('.card1').offsetWidth + 20;
      updateVisibleCards();
    });