const invite_friend_to_challenge_buttons =
  document.getElementsByTagName("button");
for (let button of invite_friend_to_challenge_buttons) {
  if (button.id.startsWith("inviting-"))
    button.addEventListener("click", (e) => {
      let ids = button.id.split("-");
      let id = Number(ids[1]);
      let challenge_id = Number(ids[2]);

      fetch("https://127.0.0.1:5000/friends/invite", {
        method: "POST",
        headers: {
          "Content-type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ friend: id, challenge_id: challenge_id }),
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
          if (e.target.innerText == "Invite Friend to join") {
            e.target.innerText = "Invitation sent";
          }
          location.reload();
        })
        .catch((err) => console.error(err));

      // TODO: change after checking if response was ok

      // Get ID of Clicked Element
    });
}
