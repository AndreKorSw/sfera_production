ymaps.ready(init);

function init() {
    var geolocation = ymaps.geolocation,
        myMap = new ymaps.Map('map', {
            center: [55.751574, 37.573856],
            zoom: 10,
            controls: ['geolocationControl']
        }, {
            searchControlProvider: 'yandex#search'
        });

    myGeoObjects = [];

    $.getJSON("/company.json", function(json){
        for (i = 0; i < json.length; i++) {
            myPlacemark = new ymaps.Placemark(
              [json[i].latitude, json[i].longitude], {
                balloonContentHeader: '<a class="js_map_link" href = "show_post/{0}">'.f(json[i].slug)+ json[i].title +'</a><br><span class="description">'+ json[i].address +'</span>',
//                balloonContentBody: '<span class="description">'+ json[i].cat +'</span>',
                balloonContentFooter: '<a href="tel:'+ json[i].phone +'">'+ json[i].phone +'</a><br><div class="description">'+ "м." + json[i].metro +'</div>',

//                hintContent: json[i].slug
             },
             {
                iconColor: '#e451fe',
             }
             );
            myGeoObjects.push(myPlacemark);
        }
        clusterer = new ymaps.Clusterer(
        { preset: 'islands#invertedPinkClusterIcons',
        });

        clusterer.options.set({gridSize: 100, minClusterSize:2, synchAdd:true});
        clusterer.add(myGeoObjects);
        myMap.geoObjects.add(clusterer);
    }).fail(function(jqXHR) {
        if (jqXHR.status == 404) {
            console.log("404 Not Found");
        } else {
            console.log("Other non-handled error type");
        }
    });
    
    geolocation.get({
        provider: 'browser',
        mapStateAutoApply: true
    }).then(function (result) {
        result.geoObjects.options.set('preset', 'islands#violetCircleIcon');
        result.geoObjects.get(0).properties.set({
            balloonContentBody: 'Мое местоположение'
        });
        myMap.geoObjects.add(result.geoObjects);
    });

}

String.prototype.format = String.prototype.f = function(){
	var args = arguments;
	return this.replace(/\{(\d+)\}/g, function(m,n){
		return args[n] ? args[n] : m;
	});
};