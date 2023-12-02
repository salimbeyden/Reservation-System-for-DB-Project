document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize variables
    let currentIndex = 0;

    var slideshowImage = document.getElementById('slideshow-image');
    var slideshowText = document.getElementById('slideshow-text');
    
    var prevButton = document.getElementById('prev');
    var nextButton = document.getElementById('next');

    slideContent = [
        {"id": "ayazaga",   "alt": "Ayazağa",   "sports": ["basketball", "volleyball", "tennis"],   "caption": "Ayazağa Campus, the main settlement, is in the Maslak region, which has become the new business and trade center of Istanbul. Covering an area of 1,600,000 m2, Ayazağa Campus includes 8 out of 13 faculties and 6 institutes, as well as the Rectorate and administrative units. Mustafa İnan Central Library, which is open 24/7 on this campus, Central Classroom buildings and 75. Yıl Student Social Center constitute the dense living areas of the campus. There are 13 dormitories on campus with a total capacity of 3882 students. There is also a Medico Health Center, a stadium with a capacity of 5100 people, an Olympic pool, various cafes and an artificial pond.", "transportation": "You can use the metro line <m2>M2 Yenikapı - Hacıosman</m2> and the İETT busses."},
        {"id": "gumussuyu", "alt": "Gümüşsuyu", "sports": ["volleyball", "tennis"],                 "caption": "Gümüşsuyu Campus, together with Taşkışla Campus, is in the Taksim region, which was the most important trade and cultural center in 19th century Istanbul and continues the same functions today. It has an area of 42,660 m2. Within the campus; There are Faculty of Mechanical Engineering, Faculty of Textile Technologies and Design, Faculty of Mechanical Engineering Ratip Berker Library, indoor sports hall and outdoor sports fields, dining hall, dormitory for girls and boys.", "transportation": "You can use the metro line <m2>M2 Yenikapı - Hacıosman</m2>, the funicular line <f1>F1 Taksim - Kabataş</f1> and the İETT busses."},
        {"id": "macka",     "alt": "Maçka",     "sports": ["basketball", "football", "volleyball"], "caption": "Education started in the 1970s at the Maçka Campus, which was built as a Police Station during the Ottoman Empire. It has an area of 63,009 m2. Inside the campus, which is a city campus; There are the Faculty of Business Administration, School of Foreign Languages, Turkish Music State Conservatory, Music Advanced Research Center Library, School of Foreign Languages Library, Faculty of Business Administration Library, Conservatory Library, ITU Foundation offices, ITU Social Facilities and cafeteria. There is a cable car line between Taşkışla Campus.", "transportation": "You can use the lift <tf1>TF1 Maçka - Taşkışla</tf1> to transfer between the Maçka and Taşkışla campuses."},
        {"id": "taskisla",  "alt": "Taşkışla",  "sports": ["basketball", "football", "tennis"],     "caption": "The campus was built as a hospital for Mekteb-i Tıbbiye-i Şahane (Military Medical School) between 1846 and 1852 by the British architect Williams James Smith and his assistant Ottoman journeyman İstefan. The campus, which was used as a barracks in 1860, was given to the Ministry of Education (Ministry of Education) after the Republic; In 1950, ITU Rectorate, Architecture and Construction Faculties were established and started to serve. It has an area of 52,252 m2. Taşkışla Campus includes the Faculty of Architecture, Department of Fine Arts and Continuing Education Center, as well as the Faculty of Architecture Library and the cafeteria.", "transportation": "You can use the metro line <m2>M2 Yenikapı - Hacıosman</m2>, the funicular line <f1>F1 Taksim - Kabataş</f1>, the İETT busses as well as the lift <tf1>TF1 Maçka - Taşkışla</tf1> to transfer between the Maçka and Taşkışla campuses."},
        {"id": "tuzla",     "alt": "Tuzla",     "sports": ["basketball", "football"],               "caption": "It started education in 1992 with the establishment of ITU Maritime Faculty. It has an area of 66,142 m2. The campus, which is a city campus, includes the Maritime Faculty, the Maritime Faculty Library, Captain Altay Altuğ Laboratory and Dining Hall Building, real maneuver boats instead of simulations, a sea survival laboratory with a capacity of 25 people, an indoor training and swimming pool, 33 m long and 17 m wide. There is a training pool with the largest wave simulation function, a dining hall and a dormitory.", "transportation": "You can use İETT busses."}
    ];

    slideLength = slideContent.length;

    // Create a function to generate a list from an array
    function createList(array) {
        var ul = document.createElement("ul");
        array.forEach(function(item) {
            var li = document.createElement("li");
            li.textContent = item;
            ul.appendChild(li);
        });
        return ul;
    }

    // Update the slideshow with the current item
    function updateSlideshow() {
        // Check if data is loaded
        if (!slideContent || slideContent.length === 0) return;
        item = slideContent[currentIndex];
        
        slideshowText.innerHTML = "<h1>" + item.alt + "</h1><p>"
                                + item.caption
                                + "</p><h3>Transportation:</h3><p>"
                                + item.transportation
                                + "</p><h2>Sports Avaliable:</h2>";
        slideshowText.appendChild(createList(item.sports))
        var baseImageUrl = document.getElementById('slideshow').dataset.baseImageUrl;
        slideshowImage.src = baseImageUrl + item.id + ".png";
        //slideshowImage.src = "./images/campus/" + item.id + ".png";
    }

    // Change the slideshow to the next item
    function moveToNextSlide() {
        if (currentIndex < slideLength - 1) {
            currentIndex++;
        } else {
            currentIndex = 0;
        }
        updateSlideshow();
    }

    // Change the slideshow to the previous item
    function moveToPrevSlide() {
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            currentIndex = slideLength - 1;
        }
        updateSlideshow();
    }

    // Change the slideshow using buttons
    prevButton.addEventListener('click', moveToPrevSlide);
    nextButton.addEventListener('click', moveToNextSlide);

    // Change the slideshow periodically
    setInterval(moveToNextSlide, 5000);

    updateSlideshow();
});