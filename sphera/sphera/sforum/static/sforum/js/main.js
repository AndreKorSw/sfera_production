ymaps.ready(init);

function init() {
    var geolocation = ymaps.geolocation,
        myMap = new ymaps.Map('map', {
            center: [55.751574, 37.573856], // начальный центр карты
            zoom: 10, // начальный уровень масштабирования
            controls: ['geolocationControl', 'zoomControl'] // добавляем стандартный контроль зума
        }, {
            searchControlProvider: 'yandex#search'
        });

    var myGeoObjects = []; // Массив для объектов компании
    var myEventObjects = []; // Массив для объектов событий

    // Загрузка данных компаний
    $.getJSON("/company.json", function(json) {
        for (i = 0; i < json.length; i++) {
            var myPlacemark = new ymaps.Placemark(
                [json[i].latitude, json[i].longitude], {
                    balloonContentHeader: '<a class="js_map_link" href="show_post/{0}">'.f(json[i].slug) + json[i].title + '</a><br><span class="description">' + json[i].address + '</span>',
//                    balloonContentBody: '<span class="description">' + json[i].__cat.name + '</span>',
                    balloonContentFooter: '<a href="tel:' + json[i].phone + '">' + json[i].phone + '</a><br><div class="description">' + "м." + json[i].metro + '</div>',
                }, {
                    iconColor: '#e451fe', // Цвет для компаний
                }
            );
            myGeoObjects.push(myPlacemark); // Добавляем метку компании в массив
        }

        // Создаем кластер для компаний
        var clusterer = new ymaps.Clusterer({
            preset: 'islands#invertedPinkClusterIcons',
        });

        clusterer.options.set({ gridSize: 100, minClusterSize: 2, synchAdd: true });
        clusterer.add(myGeoObjects); // Добавляем компании в кластер
        myMap.geoObjects.add(clusterer); // Добавляем кластер на карту
    }).fail(function(jqXHR) {
        if (jqXHR.status == 404) {
            console.log("404 Not Found");
        } else {
            console.log("Other non-handled error type");
        }
    });

    // Загрузка данных событий
    $.getJSON("/events.json", function(json) {
        for (i = 0; i < json.length; i++) {
            var myPlacemark = new ymaps.Placemark(
                [json[i].latitude, json[i].longitude], {
                    balloonContentHeader: '<a class="js_map_link" href="show_event/{0}">'.f(json[i].slug) + json[i].title + '</a>',
                    balloonContentBody: '<div class="description">' + json[i].content + '</div>',
                }, {
                    // Используем локально сохраненную иконку пламени
                    iconLayout: 'default#image',
                    iconImageHref: 'https://img.icons8.com/emoji/48/fire.png', // Путь к скаченной иконке (предположим, она лежит в папке images)
                    iconImageSize: [40, 40], // Размер иконки
                    iconImageOffset: [-20, -40] // Смещение иконки
                }
            );
            myEventObjects.push(myPlacemark); // Добавляем метку события в массив
        }

        // Создаем кластер для событий
        var eventClusterer = new ymaps.Clusterer({
            preset: 'islands#invertedBlueClusterIcons',
        });

        eventClusterer.options.set({ gridSize: 100, minClusterSize: 2, synchAdd: true });
        eventClusterer.add(myEventObjects); // Добавляем события в кластер
        myMap.geoObjects.add(eventClusterer); // Добавляем кластер на карту
    }).fail(function(jqXHR) {
        if (jqXHR.status == 404) {
            console.log("404 Not Found");
        } else {
            console.log("Other non-handled error type");
        }
    });

    // Геолокация
    geolocation.get({
        provider: 'browser',
        mapStateAutoApply: true
    }).then(function(result) {
        result.geoObjects.options.set('preset', 'islands#violetCircleIcon');
        result.geoObjects.get(0).properties.set({
            balloonContentBody: 'Мое местоположение'
        });
        myMap.geoObjects.add(result.geoObjects);
    });

    // Добавление контроля масштабирования
    myMap.controls.add('zoomControl', {
        size: 'small', // Маленький размер для управления масштабом
        float: 'none', // Контрол будет располагаться внутри карты, а не сбоку
        position: { top: 10, left: 10 } // Позиция на карте
    });
}

// Строка форматирования
String.prototype.format = String.prototype.f = function() {
    var args = arguments;
    return this.replace(/\{(\d+)\}/g, function(m, n) {
        return args[n] ? args[n] : m;
    });
};
