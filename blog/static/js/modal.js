
function registerModalEvents(trigger) {
    let overlay = document.querySelector(trigger.dataset.mdTrigger) || document.querySelector(trigger.dataset.mdCloseTrigger);
    let overlayBody = overlay.querySelector(".md-overlay-body");

    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) {
        toggleModal(overlay, overlayBody);
      }
    });

    trigger.addEventListener("click", function (e) {
      e.preventDefault();
      toggleModal(overlay, overlayBody);
    });
}

function toggleModal(overlay, overlayBody) {
  overlay.classList.toggle("hidden");
  overlay.classList.toggle("bg-opacity-0");
  overlay.classList.toggle("bg-opacity-60");
  overlayBody.classList.toggle("opacity-0");
  overlayBody.classList.toggle("opacity-100");
  overlayBody.classList.toggle("duration-500");
  overlay.classList.toggle("flex");
}

let modalTriggers = document.querySelectorAll("[data-md-trigger]")
let modalCloseTriggers = document.querySelectorAll("[data-md-close-trigger]");

modalTriggers.forEach((trigger) => {
  registerModalEvents(trigger)
});
modalCloseTriggers.forEach((trigger) => {
  registerModalEvents(trigger)
});