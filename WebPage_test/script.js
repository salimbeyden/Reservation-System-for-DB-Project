document.addEventListener('DOMContentLoaded', () => {
    const jsForm = document.querySelector('form');
    const jsSubmitButton = document.getElementById('js-submit-button');
    const statusMessage = document.getElementById('reservation-status');

    jsSubmitButton.addEventListener('click', () => {
        const name = document.getElementById('name').value;
        const facility = document.getElementById('facility').value;
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;

        const message = `Reservation made by ${name} for ${facility} on ${date} at ${time}`;
        statusMessage.textContent = message;
    });
});
