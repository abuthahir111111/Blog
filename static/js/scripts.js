let card_container = document.querySelector(".cards");
let blog_page = 1 // 1 for blog, 2 for about and 3 for contact. It corresponds to nav links in the nav bar to specify which nav link is active
let all_nav_links = document.querySelectorAll(".links>ul>li>a");
// For the slide show in header
let blog_container = document.querySelector(".blog-container");



function changeButtonsToLinks(...collections) {
    for (let buttons of collections) {
        if (!buttons) break;
        for (let button of buttons) {
            button.addEventListener('click', function(evt) {
                evt.stopPropagation();
                window.location = button.getAttribute("href");
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
for (let blog of blogs) {
    blog.addEventListener("mouseover", function(evt) {
        evt.stopPropagation();
        let privilege_buttons = blog.children[3];
        privilege_buttons.style.opacity = 1;
    });
    blog.addEventListener("mouseout", function(evt) {
        evt.stopPropagation();
        let privilege_buttons = blog.children[3];
        privilege_buttons.style.opacity = 0;
    });
}


// render background of sections
let sections = document.querySelectorAll("section");
for (let section of sections) {
    section.style.backgroundImage = `url(${section.getAttribute('img_url')})`;
    section.style.backgroundSize = `cover`;
    section.style.backgroundPosition = `50% 50%`;
}

// burger icon javascript
let menuIcon = document.querySelector(".burger-icon");
menuIcon.isOpen = false;
let links = document.querySelector(".links");
menuIcon.addEventListener('click',function(evt) {
    if (!menuIcon.isOpen) {
        links.classList.toggle("burger-icon-links");
        links.classList.toggle("links");
    }
});


// changing delete post's default behavior
let deletePosts = document.querySelectorAll(".delete-post");
let popupWarning = document.querySelector(".popup-warning"); 
let confirmButton = document.querySelector(".confirm");
let reject = document.querySelector(".reject");
if (reject) {
    reject.addEventListener('click', function(evt) {
        evt.preventDefault();
        popupWarning.style.opacity = 0;
        popupWarning.style.display = "none";
        document.body.classList.remove("stop-scrolling");
    });
}
for (let deletePost of deletePosts) {
    if (!deletePost) break;
    deletePost.addEventListener('click', function(evt) {
        evt.preventDefault();
        evt.stopPropagation();
        popupWarning.style.display = "block";
        popupWarning.style.opacity = 1;
        confirmButton.href = deletePost.href;
        document.body.classList.add("stop-scrolling");
    });
}
if (confirmButton) {
    confirmButton.addEventListener('click', (evt) => {
        document.body.classList.remove("stop-scrolling");
    });
}