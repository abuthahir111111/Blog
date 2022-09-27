let card_container = document.querySelector(".cards");
let blog_page = 1 // 1 for blog, 2 for about and 3 for contact. It corresponds to nav links in the nav bar to specify which nav link is active
let all_nav_links = document.querySelectorAll(".links>ul>li>a");
// For the slide show in header
let blog_container = document.querySelector(".blog-container");



function changeButtonsToLinks(...collections) {
    for (let buttons of collections) {
        for (let button of buttons) {
            button.addEventListener('click', (evt) => {
                window.location=button.getAttribute("href");
            });
        }
    }
}


// opacity changing slideshow
if (card_container) {
    let currentCard = 2;
    let num_images = 3;
    let cards = card_container.children;
    setInterval(()=>{
        cards[(currentCard + 0) % num_images].style.opacity = 1;
        for (let i=1; i<num_images; ++i) {
            cards[(currentCard + i) % num_images].style.opacity = 0;
        }
        currentCard += 1;
    }, 4000);
}



// changing all blog thumbnails to links
let blogs = document.querySelectorAll(".blog");
let sign_in_buttons = document.querySelectorAll('.sign-up');
let log_in_buttons = document.querySelectorAll(".log-in");
changeButtonsToLinks(blogs, sign_in_buttons, log_in_buttons);
