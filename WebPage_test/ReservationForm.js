import React, { useState } from 'react';

function ReservationForm() {
    const [name, setName] = useState('');
    const [facility, setFacility] = useState('facility1');
    const [date, setDate] = useState('');
    const [time, setTime] = useState('');

    const handleSubmit = () => {
        const message = `Reservation made by ${name} for ${facility} on ${date} at ${time}`;
        // You can send this message to a backend, but for this example, we're just logging it.
        console.log(message);
    };
}



export default ReservationForm;
