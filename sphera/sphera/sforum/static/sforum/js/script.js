
document.querySelector('.burger').addEventListener('click', function() {
            this.classList.toggle('active');
            document.querySelector('.header__menu').classList.toggle('open');
        })

const isMobile = {
	Android: function () {
		return navigator.userAgent.match(/Android/i);
	},
	BlackBerry: function () {
		return navigator.userAgent.match(/BlackBerry/i);
	},
	iOS: function () {
		return navigator.userAgent.match(/iPhone|iPad|iPod/i);
	},
	Opera: function () {
		return navigator.userAgent.match(/Opera Mini/i);
	},
	Windows: function () {
		return navigator.userAgent.match(/IEMobile/i);
	},
	any: function () {
		return (
			isMobile.Android() ||
			isMobile.BlackBerry()||
			isMobile.iOS() ||
			isMobile.Opera() ||
			isMobile.Windows());
	}
};

if (isMobile.any()) {
	document.body.classList.add("_touch");

	let filterArrows = document.querySelectorAll('.filter__arrow');
	if (filterArrows.length > 0) {
		for (let index = 0; index < filterArrows.length; index++){
			const filterArrow = filterArrows[index];
			filterArrow.addEventListener("click", function (e){
				filterArrow.parentElement.classList.toggle('_active');
			});
		}
	}

} else {
	document.body.classList.add("_pc");
}

document.querySelector('.action__link-black').addEventListener('click', function() {
            this.classList.toggle('active');
            document.querySelector('.header__menu').classList.toggle('open');
        })





