    function shareContent(url) {
        if (navigator.share) {
            navigator.share({
                title: 'Посетите эту новость',
                text: 'Я нашел интересную новость, думаю, вам тоже понравится!',
                url: url
            })
            .then(() => console.log('Ссылка была успешно поделена!'))
            .catch((error) => console.log('Ошибка при попытке поделиться', error));
        } else {
            alert('К сожалению, ваше устройство не поддерживает функцию общего доступа.');
        }
    }