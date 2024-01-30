const add_buttons = document.getElementsByTagName("button");

const acceptEvent = (e) => {
  let id = Number(e.target.id.replace("accept-", ""));
  console.log(id);

  fetch("https://127.0.0.1:5000/friends/accepting", {
    method: "POST",
    headers: {
      "Content-type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({ friend: id }),
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

      // TODO: change after checking if response was ok
      console.log(id);
      if (e.target.innerText == "Accept") {
        e.target.innerText = "Accepting";
      }
      location.reload();
    })
    .catch((err) => console.error(err));

  // Get ID of Clicked Element
};
for (let btn of add_buttons) {
  if (btn.id.startsWith("accept-")) btn.addEventListener("click", acceptEvent);
}
