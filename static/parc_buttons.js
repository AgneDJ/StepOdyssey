const buttons = document.getElementsByTagName("button");

const buttonPressed = (e) => {
  let id = Number(e.target.id.replace("participate-", ""));
  fetch("https://stepodyssey.com/challenges", {
    method: "POST",
    headers: {
      "Content-type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({ id: id }),
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
    })
    .catch((err) => console.error(err));

  // TODO: change after checking if response was ok
  console.log(id);
  if (e.target.innerText == "Participate") {
    e.target.innerText = "Joined";
  }

  // Get ID of Clicked Element
};
for (let button of buttons) {
  if (button.id.startsWith("participate-"))
    button.addEventListener("click", buttonPressed);
}
