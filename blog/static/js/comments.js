const commentInput = document.getElementById("comment-input");
commentContent = commentInput.querySelector("textarea");
commentContent.addEventListener("input", () => {
    const charCount = document.getElementById("char-count-num");
    charCount.innerText = commentContent.value.length;
});

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}