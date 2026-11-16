// Быстрый фильтр карточек мест на странице списка (без перезагрузки).
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("place-filter");
  if (!input) return;
  const cards = document.querySelectorAll(".rs-place");
  const empty = document.getElementById("place-filter-empty");
  input.addEventListener("input", () => {
    const text = input.value.trim().toLowerCase();
    let shown = 0;
    cards.forEach((card) => {
      const match = card.dataset.search.includes(text);
      card.classList.toggle("d-none", !match);
      if (match) shown += 1;
    });
    empty.classList.toggle("d-none", shown > 0);
  });
});
