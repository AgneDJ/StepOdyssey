const message = document.getElementById("message_text");
const button = document.getElementById("submit");

button.addEventListener("click", (e) => {
  e.preventDefault();
  fetch("https://stepodyssey.com/contact_mes", {
    method: "POST",
    headers: {
      "Content-type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({ message: message.value }),
  })
    .then((res) => {
      if (res.ok) {
        return res.json();
      } else {
        alert("Something is wrong");
      }
    })
    .then((jsonResponse) => {
      // Log the response data in the console
      console.log(jsonResponse);

      if (e.target.innerText == "Submit") {
        e.target.innerText = "Submitted";
      }
      location.reload();
    })
    .catch((err) => console.error(err));

  // TODO: change after checking if response was ok

  // Get ID of Clicked Element
});
