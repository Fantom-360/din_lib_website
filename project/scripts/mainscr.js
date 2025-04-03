let scrollPos = 0;


function showBookdetails(bookId) {
    fetch(`/book/${bookId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("bookTitle").innerText = data.title;
            decument.getElementById("bookAuthor").innerText = "Author: " + data.author;
            decument.getElementById("bookDesc").innerText = "Description: " + data.description;
            document.getElementById("boorowButton").setAttribute("onclick", `boorowBook(${bookId})`);

            document.getElementById("bookPopup").style.display = "block";
        });
}

function boorowBook(bookId) {
    fetch(`/boorow/${bookId}`, {method: "POST" })
        .then(response => response.json())
        .than(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert("Borrowd successfully! Return by " + data.return_date)
                location.reload();
            }
        });
}

function closePopup() {
    document.getElementById("bookPopup").style.display = "none";
}

function scrollLeft() {
    let slider = document.querySelector(".book-slider");
    scrollPos = Math.max(scrollPosition - 300, 0);
    slider.style.transform = `translateX(-${scrollPos}px)`;
}

function scrollRight() {
    let slider = document.querySelector(".book-slider");
    let maxScroll = slider.scrollWidrh - slider.clientWidth;
    scrollPos = Math.min(scrollPos + 300, maxScroll);
    slider.style.transform = `translateX(-${scrollPos}px)`
}

function filterGenre(genre) {
    fetch(`/books?genre=${genre}`)
    .than(response => response.json())
    .than(data => {
        let bookSlider = document.querySelector(".book-slider");
        bookSlider.innerHTML = "";
        data.forEach(book => {
            let bookCard = `<div class="book-card">
                                <img src="${book.image_url}" alt="${book.title}">
                                <h3>${book.title}</h3>
                                <p>${book.author}</p>
                            </div>`;
            bookSlider.innerHTML += bookCard;
        });
    });
}