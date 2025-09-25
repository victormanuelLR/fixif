function closeErrorModal() {
  const modal = document.getElementById("errorModal");
  if (modal) {
    modal.classList.remove("show");
    setTimeout(() => {
      modal.style.display = "none";
    }, 300);
  }
}
document.addEventListener("DOMContentLoaded", function () {
  const errorModal = document.getElementById("errorModal");
  if (errorModal) {
    setTimeout(() => {
      errorModal.classList.add("show");
    }, 100);
  }

  errorModal?.addEventListener("click", function (e) {
    if (e.target === errorModal) {
      closeErrorModal();
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && errorModal?.classList.contains("show")) {
      closeErrorModal();
    }
  });
});

function togglePassword() {
  const passwordInput = document.getElementById("password");
  const passwordIcon = document.getElementById("passwordIcon");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    passwordIcon.className = "bi bi-eye-slash";
  } else {
    passwordInput.type = "password";
    passwordIcon.className = "bi bi-eye";
  }
}

document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault();

  if (!username || !password) {
    alert("Por favor, preencha todos os campos.");
    return;
  }

  loginBtn.classList.add("btn-loading");
  loginBtn.disabled = true;
  this.submit();
});

document.querySelectorAll(".form-control-modern").forEach((input) => {
  input.addEventListener("focus", function () {
    this.parentElement.classList.add("focused");
  });

  input.addEventListener("blur", function () {
    this.parentElement.classList.remove("focused");
  });
});
