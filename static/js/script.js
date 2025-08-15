// Only add event listener if the download button exists (main page)
const downloadButton = document.getElementById('button-download');
if (downloadButton) {
  downloadButton.addEventListener('click', function () {
    this.style.display = 'none';
    const spinner = document.getElementById('spinner');
    if (spinner) {
      spinner.style.display = 'block';
    }
  });
}

document.body.addEventListener('htmx:afterSettle', function (event) {
  if (event.target.id === "result") {
    let successCard = document.getElementById('success-card');
    if (successCard) {
      showSuccessCard();
    }

    setTimeout(function () {
      window.location.reload();
    }, 3000);
  }
});

function showSuccessCard() {
  const card = document.getElementById("success-card");
  if (!card) return;

  card.classList.remove("hide");
  card.classList.add("show");

  card.style.display = "block";

  setTimeout(() => {
    card.classList.remove("show");
    card.classList.add("hide");

    setTimeout(() => {
      card.style.display = "none";
    }, 400);
  }, 2500);
}
