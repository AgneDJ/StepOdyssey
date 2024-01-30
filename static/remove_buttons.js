const buttons = document.getElementsByTagName("button");

const removeEvent = (e) => {
  let id = Number(e.target.id.replace("remove-", ""));
  console.log(id);
  console.log(e.target.id);

  fetch("https://127.0.0.1:5000/friends/notadding", {
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
      console.log(id);
      if (e.target.innerText == "Remove") {
        e.target.innerText = "Removing";
      }
      location.reload();
    })
    .catch((err) => console.error(err));

  // TODO: change after checking if response was ok

  // Get ID of Clicked Element
};
for (let button of buttons) {
  if (button.id.startsWith("remove-"))
    button.addEventListener("click", removeEvent);
}
