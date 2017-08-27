$(function () {
    initAjaxCsrf();
    initGallery();
    initLikes();
    initFlags();
});

function initGallery() {
    var pswpElement = document.querySelectorAll('.pswp')[0];

    var photoElements = $('.photo');

    var items = photoElements.toArray().map(function (photoElement) {
        var photo = $(photoElement);
        return {
            src: photo.attr('src'),
            w: photo.data('width'),
            h: photo.data('height'),
            photoId: photo.data('id'),
            likes: photo.data('likes'),
            title: true
        }
    });

    photoElements.click(function (event) {
        var options = {
            index: photoElements.index(event.target),
            shareEl: false,
            captionEl: true,
            addCaptionHTMLFn: function (item, captionEl, isFake) {
                captionEl.children[0].innerHTML = '<a class="gallery-button like-button" data-id="' + item.photoId + '"><span class="icon is-small">' +
                    '<i class="fa fa-heart"></i>' +
                    '</span>&nbsp;' +
                    '<span class="like-count">' + item.likes + '</span>' +
                    '</a>' +
                    '<a class="gallery-button" href="/photo/' + item.photoId + '/">Details</a>';
                initLikes();
                return true;
            }
        };

        var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
        gallery.init();
    });
}

function initLikes() {
    var likeButtons = $('.like-button');
    likeButtons.off('click');
    likeButtons.click(function (event) {
        var likeButton = $(event.target).closest('.like-button');
        var photoId = likeButton.data('id');
        $.ajax({
            url: '/photos/like/',
            type: 'POST',
            data: {'photo_id': photoId},
            success: function (result) {
                likeButton.find('.like-count').text(result);
            },
            error: function (result) {
                alert("Error :(")
            }
        });
    });
}

function initFlags() {
    $('.flag-button').click(function (event) {
        var flagButton = $(event.target).closest('.flag-button');
        var photoId = flagButton.data('id');

        $.ajax({
            url: '/photos/flag/',
            type: 'POST',
            data: {'photo_id': photoId},
            success: function (result) {
                alert("Photo has been reported. Thanks!");
            },
            error: function (result) {
                alert("Error :(")
            }
        });
    });
}

function initAjaxCsrf() {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", window.csrfToken);
            }
        }
    });
}