document.querySelectorAll(".filter-btn").forEach((btn) => {
  btn.addEventListener("click", function (e) {
    e.preventDefault();

    document
      .querySelectorAll(".filter-btn")
      .forEach((b) => b.classList.remove("active"));

    this.classList.add("active");
  });
});

document.querySelector(".search-input").addEventListener("input", function (e) {
  const searchTerm = e.target.value.toLowerCase();
});

document.querySelectorAll(".action-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    const action = this.title;
    const ticketCard = this.closest(".ticket-card");
    const ticketId = ticketCard.querySelector(".ticket-id").textContent;

    if (action === "Ver detalhes") {
      window.location.href = `ticket-details.html?id=${ticketId}`;
    } else if (action === "Comentar") {
      alert(`Comentar no chamado ${ticketId}`);
    }
  });
});

function simulateRealTimeUpdates() {
  setInterval(() => {
    document.querySelectorAll(".meta-item").forEach((item) => {
      if (item.textContent.includes("Há")) {
      }
    });
  }, 60000);
}

document.querySelectorAll(".like-btn").forEach((btn) => {
  btn.addEventListener("click", async function (e) {
    e.preventDefault();
    const reportId = this.dataset.reportId;
    const icon = this.querySelector("i");
    const countSpan = this.querySelector(".like-count");

    try {
      const response = await fetch(`/api/report/${reportId}/like/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();

      if (data.success) {
        if (data.liked) {
          this.classList.add("liked");
          icon.classList.remove("bi-heart");
          icon.classList.add("bi-heart-fill");
        } else {
          this.classList.remove("liked");
          icon.classList.remove("bi-heart-fill");
          icon.classList.add("bi-heart");
        }
        countSpan.textContent = data.like_count;
      }
    } catch (error) {}
  });
});

document.querySelectorAll(".comment-like-btn").forEach((btn) => {
  btn.addEventListener("click", async function (e) {
    e.preventDefault();
    const commentId = this.dataset.commentId;
    const icon = this.querySelector("i");
    const countSpan = this.querySelector(".comment-like-count");

    try {
      const response = await fetch(`/api/comment/${commentId}/like/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();

      if (data.success) {
        if (data.liked) {
          this.classList.add("liked");
          icon.classList.remove("bi-heart");
          icon.classList.add("bi-heart-fill");
        } else {
          this.classList.remove("liked");
          icon.classList.remove("bi-heart-fill");
          icon.classList.add("bi-heart");
        }
        countSpan.textContent = data.like_count;
      }
    } catch (error) {
      console.error(" error:", error);
    }
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.querySelectorAll(".comment-toggle-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    const reportId = this.dataset.reportId;
    const commentForm = document.getElementById(`comment-form-${reportId}`);
    commentForm.classList.toggle("active");

    if (commentForm.classList.contains("active")) {
      const textarea = commentForm.querySelector(".comment-input");
      textarea.focus();
    }
  });
});

document.querySelectorAll(".comment-submit-btn").forEach((btn) => {
  btn.addEventListener("click", async function () {
    const reportId = this.dataset.reportId;
    const textarea = document.querySelector(
      `.comment-input[data-report-id="${reportId}"]`
    );
    const content = textarea.value.trim();

    if (!content) {
      alert("Por favor, escreva um comentário");
      return;
    }

    this.disabled = true;

    try {
      const response = await fetch(`/api/report/${reportId}/comment/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content }),
      });

      const data = await response.json();

      if (data.success) {
        textarea.value = "";

        document
          .getElementById(`comment-form-${reportId}`)
          .classList.remove("active");

        const commentsPreview = document.getElementById(
          `comments-preview-${reportId}`
        );
        commentsPreview.style.display = "block";

        const commentHTML = `
                            <div class="comment-item" data-comment-id="${
                              data.comment.id
                            }">
                                <div class="comment-header">
                                    <div class="comment-author">
                                        <div class="comment-avatar">${
                                          data.comment.user_initial
                                        }</div>
                                        <span class="comment-author-name">${
                                          data.comment.user_nickname
                                        }</span>
                                        <span class="comment-time">${
                                          data.comment.created_at
                                        }</span>
                                    </div>
                                    ${
                                      data.comment.is_author
                                        ? `
                                        <button class="comment-delete-btn" data-comment-id="${data.comment.id}">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    `
                                        : ""
                                    }
                                </div>
                                <p class="comment-content">${
                                  data.comment.content
                                }</p>
                                <div class="comment-actions">
                                    <button class="comment-like-btn" data-comment-id="${
                                      data.comment.id
                                    }">
                                        <i class="bi bi-heart"></i>
                                        <span class="comment-like-count">0</span>
                                    </button>
                                </div>
                            </div>
                        `;

        commentsPreview.insertAdjacentHTML("afterbegin", commentHTML);

        const commentBtn = document.querySelector(
          `.comment-toggle-btn[data-report-id="${reportId}"] span`
        );
        const currentCount = parseInt(commentBtn.textContent);
        commentBtn.textContent = currentCount + 1;

        attachCommentEventListeners();
      } else {
        alert(data.error || "Erro ao criar comentário");
      }
    } catch (error) {
      console.error("error :", error);
      alert("Erro ao criar comentário");
    } finally {
      this.disabled = false;
    }
  });
});

function attachCommentEventListeners() {
  document.querySelectorAll(".comment-delete-btn").forEach((btn) => {
    const clonedBtn = btn.cloneNode(true);
    btn.parentNode.replaceChild(clonedBtn, btn);
  });

  document.querySelectorAll(".comment-delete-btn").forEach((btn) => {
    btn.addEventListener("click", async function () {
      if (!confirm("Deseja este comentário?")) {
        return;
      }

      const commentId = this.dataset.commentId;

      try {
        const response = await fetch(`/api/comment/${commentId}/delete/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();

        if (data.success) {
          const commentItem = document.querySelector(
            `.comment-item[data-comment-id="${commentId}"]`
          );
          const reportCard = commentItem.closest(".ticket-card");
          const reportId = reportCard.dataset.reportId;

          commentItem.remove();

          const commentBtn = reportCard.querySelector(
            ".comment-toggle-btn span"
          );
          const currentCount = parseInt(commentBtn.textContent);
          commentBtn.textContent = Math.max(0, currentCount - 1);

          const commentsPreview = document.getElementById(
            `comments-preview-${reportId}`
          );
          if (commentsPreview.children.length === 0) {
            commentsPreview.style.display = "none";
          }
        } else {
          alert(data.error || "Erro ao deletar comentário");
        }
      } catch (error) {
        alert("Erro ao deletar comentário");
      }
    });
  });

  document.querySelectorAll(".comment-like-btn").forEach((btn) => {
    const clonedBtn = btn.cloneNode(true);
    btn.parentNode.replaceChild(clonedBtn, btn);
  });

  document.querySelectorAll(".comment-like-btn").forEach((btn) => {
    btn.addEventListener("click", async function (e) {
      e.preventDefault();
      const commentId = this.dataset.commentId;
      const icon = this.querySelector("i");
      const countSpan = this.querySelector(".comment-like-count");

      try {
        const response = await fetch(`/api/comment/${commentId}/like/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();

        if (data.success) {
          if (data.liked) {
            this.classList.add("liked");
            icon.classList.remove("bi-heart");
            icon.classList.add("bi-heart-fill");
          } else {
            this.classList.remove("liked");
            icon.classList.remove("bi-heart-fill");
            icon.classList.add("bi-heart");
          }
          countSpan.textContent = data.like_count;
        }
      } catch (error) {
        console.error("error:", error);
      }
    });
  });
}

document.querySelectorAll(".view-details-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    const reportId = this.dataset.reportId;
    window.location.href = `/report/${reportId}/`;
  });
});

document.addEventListener("DOMContentLoaded", function () {
  attachCommentEventListeners();
  simulateRealTimeUpdates();
});
