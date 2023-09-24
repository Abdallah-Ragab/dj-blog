
const switchModal = (trigger) => {
    let overlay = document.querySelector(trigger.dataset.mdTrigger) || document.querySelector(trigger.dataset.mdCloseTrigger);
    let overlayBody = overlay.querySelector(".md-overlay-body");

    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) {
        overlay.classList.toggle("hidden");
        overlay.classList.toggle("bg-opacity-0");
        overlay.classList.toggle("bg-opacity-60");
        overlayBody.classList.toggle("opacity-0");
        overlayBody.classList.toggle("opacity-100");
        overlayBody.classList.toggle("duration-500");
        overlay.classList.toggle("flex");
      }
    });

    trigger.addEventListener("click", function (e) {
      e.preventDefault();
      overlay.classList.toggle("hidden");
      overlay.classList.toggle("bg-opacity-0");
      overlay.classList.toggle("bg-opacity-60");
      overlayBody.classList.toggle("opacity-0");
      overlayBody.classList.toggle("opacity-100");
      overlayBody.classList.toggle("duration-500");
      overlay.classList.toggle("flex");
    });
}

let modalTriggers = document.querySelectorAll("[data-md-trigger]")
let modalCloseTriggers = document.querySelectorAll("[data-md-close-trigger]");
modalTriggers.forEach((trigger) => {
  switchModal(trigger)
});
modalCloseTriggers.forEach((trigger) => {
  switchModal(trigger)
});