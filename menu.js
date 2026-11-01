// Menu commun aux deux pages : déroulant « Consignes » et entrée en cours surlignée.
(function () {
  const deroulant = document.querySelector("nav.menu .deroulant");
  const fermer = () => deroulant.removeAttribute("open");

  // Refermer le déroulant après un choix, en touchant ailleurs ou avec Échap
  deroulant.querySelectorAll("a").forEach(a => a.addEventListener("click", fermer));
  document.addEventListener("click", e => { if (!deroulant.contains(e.target)) fermer(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape") fermer(); });

  const liens = [...document.querySelectorAll("nav.menu a")];
  const lien = cible => liens.find(a => a.getAttribute("href") === cible);
  function surligner(cible) {
    liens.forEach(a => a.removeAttribute("aria-current"));
    const a = lien(cible);
    if (a) a.setAttribute("aria-current", "page");
    deroulant.classList.toggle("actif", deroulant.contains(a));
  }

  if (!location.pathname.endsWith("consignes.html")) {
    surligner("index.html");
    return;
  }

  // Page des consignes : la rubrique en cours est la dernière dont le titre a passé le tiers de l'écran
  const sections = ["ouvrir", "sejour", "fermer", "contacts"].map(id => document.getElementById(id));
  function suivre() {
    const ligne = innerHeight / 3;
    let enCours = sections[0];
    sections.forEach(s => { if (s.getBoundingClientRect().top <= ligne) enCours = s; });
    // Tout en bas de page, la dernière rubrique peut ne jamais atteindre la ligne
    if (innerHeight + scrollY >= document.documentElement.scrollHeight - 2) enCours = sections[sections.length - 1];
    surligner("consignes.html#" + enCours.id);
  }
  addEventListener("scroll", suivre, { passive: true });
  addEventListener("resize", suivre);
  suivre();
})();
