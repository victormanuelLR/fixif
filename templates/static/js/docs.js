let currentIndex = 0;

if (typeof mermaid !== "undefined") {
  mermaid.initialize({ startOnLoad: false });
}

const renderDoc = (markdown) => {
  const contentDiv = document.getElementById("content");
  contentDiv.innerHTML = marked.parse(markdown);

  contentDiv.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightElement(block);
  });

  if (typeof mermaid !== "undefined") {
    const mermaidBlocks = contentDiv.querySelectorAll(
      "code.language-mermaid, pre code.language-mermaid"
    );
    mermaidBlocks.forEach((block) => {
      const parent = block.parentElement;
      const graphDefinition = block.textContent;
      const container = document.createElement("div");
      container.classList.add("mermaid");
      container.textContent = graphDefinition;
      parent.replaceWith(container);
    });

    mermaid.run();
  }

  window.scrollTo({ top: 0, behavior: "smooth" });
};

const updateNavigation = () => {
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const prevTitle = document.getElementById("prevTitle");
  const nextTitle = document.getElementById("nextTitle");

  if (currentIndex > 0) {
    prevBtn.classList.remove("disabled");
    prevTitle.textContent = docFiles[currentIndex - 1].name;
    prevBtn.onclick = (e) => {
      e.preventDefault();
      navigateToDoc(currentIndex - 1);
    };
  } else {
    prevBtn.classList.add("disabled");
    prevTitle.textContent = "-";
    prevBtn.onclick = (e) => e.preventDefault();
  }

  if (currentIndex < docFiles.length - 1) {
    nextBtn.classList.remove("disabled");
    nextTitle.textContent = docFiles[currentIndex + 1].name;
    nextBtn.onclick = (e) => {
      e.preventDefault();
      navigateToDoc(currentIndex + 1);
    };
  } else {
    nextBtn.classList.add("disabled");
    nextTitle.textContent = "-";
    nextBtn.onclick = (e) => e.preventDefault();
  }
};

const navigateToDoc = async (index) => {
  if (index < 0 || index >= docFiles.length) return;

  currentIndex = index;
  const doc = docFiles[index];

  document.querySelectorAll(".docs-nav-link").forEach((link, i) => {
    if (i === index) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }
  });

  const markdown = await loadDoc(doc.path);
  renderDoc(markdown);

  updateNavigation();


  if (window.innerWidth <= 992) {
    document.getElementById("sidebar").classList.remove("show");
  }
};

const renderSidebar = () => {
  const docsList = document.getElementById("docsList");
  docsList.innerHTML = docFiles
    .map(
      (doc, index) => `
                <li class="docs-nav-item">
                    <a href="#" class="docs-nav-link ${
                      index === 0 ? "active" : ""
                    }" data-index="${index}">
                        <i class="bi ${doc.icon}"></i>
                        <span>${doc.name}</span>
                    </a>
                </li>
            `
    )
    .join("");

  docsList.querySelectorAll(".docs-nav-link").forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const index = parseInt(link.dataset.index);
      navigateToDoc(index);
    });
  });
};

document.getElementById("sidebarToggle").addEventListener("click", () => {
  document.getElementById("sidebar").classList.toggle("show");
});

const init = async () => {
  await fetchDocDefinitions();
  renderSidebar();
  await navigateToDoc(0);
};

init();
