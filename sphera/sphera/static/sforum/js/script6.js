function shareContent(url) {
    const fullUrl = window.location.origin + url;

    if (navigator.share) {
        navigator.share({
            title: 'Посетите эту новость',
            text: 'Я нашел интересную новость, думаю, вам тоже понравится!',
            url: fullUrl
        }).then(() => console.log('Ссылка успешно поделена!'))
        .catch((error) => console.log('Ошибка при попытке поделиться', error));
    } else {
        const shareMenu = `
            <div class="share-options">
                <div class="close-share" onclick="closeShareMenu()">&times;</div>
                <a href="https://t.me/share/url?url=${encodeURIComponent(fullUrl)}" target="_blank">Поделиться в Telegram</a>
                <a href="https://vk.com/share.php?url=${encodeURIComponent(fullUrl)}" target="_blank">Поделиться в VK</a>
                <a href="https://api.whatsapp.com/send?text=${encodeURIComponent(fullUrl)}" target="_blank">Поделиться в WhatsApp</a>
                <a href="https://www.instagram.com/?url=${encodeURIComponent(fullUrl)}" target="_blank">Поделиться в Instagram</a>
                <button onclick="copyToClipboard('${fullUrl}')">Скопировать ссылку</button>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', shareMenu);
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Ссылка скопирована!');
    }).catch(err => {
        console.error('Ошибка при копировании:', err);
    });
}

function closeShareMenu() {
    const menu = document.querySelector('.share-options');
    if (menu) menu.remove();
}
