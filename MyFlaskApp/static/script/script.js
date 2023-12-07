document.addEventListener('DOMContentLoaded', function() {
    var loginForm = document.getElementById('login-form');
    var registerForm = document.getElementById('register-form');

 /*   document.getElementById('show-register').addEventListener('click', function() {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    });*/

    document.getElementById('show-login').addEventListener('click', function() {
        registerForm.style.display = 'none';
        loginForm.style.display = 'block';
    });

    document.getElementById('homepage-login').addEventListener('click', function() {
        window.location.href = "./../";
    });

    document.getElementById('homepage-register').addEventListener('click', function() {
        window.location.href = "./../";
    });
});
