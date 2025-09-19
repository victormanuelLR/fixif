let isLoggedIn = false;

function showLogin() {
  const loginModal = new bootstrap.Modal(document.getElementById("loginModal"));
  loginModal.show();
}

function updateUI() {
  const userMenu = document.getElementById("userMenu");
  const loginButtons = document.getElementById("loginButtons");

  if (isLoggedIn) {
    userMenu.classList.remove("hidden");
    loginButtons.classList.add("hidden");
  } else {
    userMenu.classList.add("hidden");
    loginButtons.classList.remove("hidden");
  }
}

function scrollToSection(sectionId) {
  document.getElementById(sectionId).scrollIntoView({
    behavior: "smooth",
  });
}

document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});

updateUI();
