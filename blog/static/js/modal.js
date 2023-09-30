
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

modalAction = document.querySelector('[data-md-action-trigger = "#md-share-via-email-modal"]')
    modal = document.querySelector('#md-share-via-email-modal')
    modalAction.addEventListener('click', e => {
        e.preventDefault()
        form = modal.querySelector('form')
        formData = new FormData(form)
        endpoint = "{% url 'blog:post_share_email' post.slug %}"
        fetch(endpoint, {
            method: 'POST',
            body: formData
        }).then(response => response.status).then(status => {
          if(status == 200){
            overlay = document.querySelector('#md-share-via-email-modal')
            overlayBody = overlay.querySelector('.md-overlay-body')

            toggleModal(overlay, overlayBody)
          }
          else if (status == 400){
            overlay = document.querySelector('#md-share-via-email-modal')
            overlayDangerAlert = overlay.querySelector('.md-massage-danger')
            overlayDangerAlertBold = overlayDangerAlert.querySelector('span')
            overlayDangerAlertMessage = overlayDangerAlert.querySelector('p')


            overlayDangerAlert.classList.remove('hidden')
            overlayDangerAlertBold.textContent = 'Failed To Send Email'
            overlayDangerAlertMessage.textContent = 'Please make sure you have filled all the fields correctly.'

          }
          else if (status == 500){
            overlay = document.querySelector('#md-share-via-email-modal')
            overlayDangerAlert = overlay.querySelector('.md-massage-danger')
            overlayDangerAlertBold = overlayDangerAlert.querySelector('span')
            overlayDangerAlertMessage = overlayDangerAlert.querySelector('p')


            overlayDangerAlert.classList.remove('hidden')
            overlayDangerAlertBold.textContent = 'Failed To Send Email'
            overlayDangerAlertMessage.textContent = 'Something went wrong. Please try again later. If the problem persists, please contact the administrator.'
          }
        })
    })