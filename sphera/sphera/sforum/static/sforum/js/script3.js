//
//let currentSlide = 0;
//const slides = document.querySelectorAll('.slide');
//const totalSlides = slides.length;
//
//function showSlide(index) {
//    slides.forEach((slide, i) => {
//        slide.classList.remove('active');
//        if (i === index) {
//            slide.classList.add('active');
//        }
//    });
//    const offset = -index * 100; // Сдвиг в процентах
//    document.querySelector('.slides').style.transform = `translateX(${offset}%)`;
//}
//
//function changeSlide(direction) {
//    currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
//    showSlide(currentSlide);
//}
//
//function autoSlide() {
//    currentSlide = (currentSlide + 1) % totalSlides;
//    showSlide(currentSlide);
//}
//
//setInterval(autoSlide, 7000); // Смена слайдов каждые 7 секунд
//showSlide(currentSlide);
//					<div class="slider">
//						<div class="slides">
//							 {% for photo_banner in banners_photo %}
//							 <div class="slide active" style="background: url('{{ photo_banner.img.url }}');">
//									<p></p>
//								</div>
//							{% endfor %}
//						</div>
//						<button class="prev_arr slide_button" onclick="changeSlide(-1)">&#10094;</button>
//        				<button class="next_arr slide_button" onclick="changeSlide(1)">&#10095;</button>
//				</div>
//.slider {
//    border-radius: 10px;
//    position: relative;
//    max-width: 100%;
//    margin: auto;
//    overflow: hidden;
//}
//
//.slides {
//    display: flex;
//    transition: transform 0.5s ease;
//}
//
//.slide {
//    min-width: 100%;
//    height: 250px; /* Фиксированная высота */
//    box-sizing: border-box;
//    display: flex;
//    justify-content: center;
//    align-items: center;
//    color: white;
//    font-size: 24px;
//    background-position: center;
//    background-repeat: no-repeat;
//    background-size: contain; /* Сохраняет пропорции изображения */
//    background-color: #000; /* Задний фон для случаев, если изображение не покрывает весь блок */
//}
//
//.slide_button {
//    position: absolute;
//    top: 50%;
//    transform: translateY(-50%);
//    background-color: rgba(255, 255, 255, 0);
//    color: rgba(255, 255, 255, 0.5);
//    border: none;
//    cursor: pointer;
//    padding: 10px;
//    font-size: 18px;
//}
//
//.prev_arr {
//    left: 10px;
//}
//
//.next_arr {
//    right: 10px;
//}

    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;

    // Функция для отображения слайда по индексу
    function showSlide(index) {
        slides.forEach((slide, i) => {
            // Перемещаем слайды за пределы видимой области
            slide.style.left = i === index ? '0' : '100%';
        });
    }

    // Функция для изменения слайда по направлению
    function changeSlide(direction) {
        currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
        showSlide(currentSlide);
    }

    // Изначально показываем первый слайд
    showSlide(currentSlide);

    // Автоматическое переключение слайдов каждые 7 секунд
    setInterval(() => {
        currentSlide = (currentSlide + 1) % totalSlides;
        showSlide(currentSlide);
    }, 7000);
