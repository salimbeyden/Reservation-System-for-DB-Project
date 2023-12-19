document.addEventListener('DOMContentLoaded', function() {

    if (document.getElementById('show-register')) {
        document.getElementById('show-register').addEventListener('click', function() {
            window.location.href = registerUrl;
        });
    }

    if (document.getElementById('homepage-login')) {
        document.getElementById('homepage-login').addEventListener('click', function() {
            window.location.href = homepageUrl;
        });
    }

    if (document.getElementById('show-login')) {
        document.getElementById('show-login').addEventListener('click', function() {
            window.location.href = loginUrl;
        });
    }

    if (document.getElementById('homepage-register')) {
        document.getElementById('homepage-register').addEventListener('click', function() {
            window.location.href = homepageUrl;
        });
    }

});
