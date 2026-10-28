// Trouillet Décors — comportements minimaux, sans framework.

document.addEventListener("DOMContentLoaded", () => {
  // Année du footer
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Menu mobile
  const toggle = document.getElementById("nav-toggle");
  const nav = document.getElementById("main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });
    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Formulaire de contact — validation simple côté client.
  // À brancher sur un service d'envoi réel (Formspree, backend, etc.)
  // avant mise en ligne : ce script ne fait qu'afficher un message local.
  const form = document.getElementById("contact-form");
  const note = document.getElementById("form-note");
  if (form && note) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.checkValidity()) {
        note.textContent = "Merci de vérifier les champs obligatoires.";
        note.style.color = "#B8703F";
        return;
      }
      note.textContent = "Message prêt à être envoyé — connectez ce formulaire à votre messagerie pour l'activer.";
      note.style.color = "";
    });
  }
});
