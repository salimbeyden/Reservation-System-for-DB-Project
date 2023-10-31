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

    return (
        <div>
            <h2>Make a Reservation (React)</h2>
            <form>
                <label htmlFor="name">Name:</label>
                <input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)} required /><br />

                <label htmlFor="facility">Facility:</label>
                <select id="facility" value={facility} onChange={(e) => setFacility(e.target.value)} required>
                    <option value="facility1">Facility 1</option>
                    <option value="facility2">Facility 2</option>
                    <option value="facility3">Facility 3</option>
                </select><br />

                <label htmlFor="date">Date:</label>
                <input type="date" id="date" value={date} onChange={(e) => setDate(e.target.value)} required /><br />

                <label htmlFor="time">Time:</label>
                <input type="time" id="time" value={time} onChange={(e) => setTime(e.target.value)} required /><br />

                <button type="button" onClick={handleSubmit}>Submit Reservation (React)</button>
            </form>
        </div>
    );
}

export default ReservationForm;
