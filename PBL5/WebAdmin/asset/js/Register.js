const patch = "http://localhost:1994/";
function onRegister() {
  let username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var re_password = document.getElementById("re_password").value;
  if (re_password != password) {
    swal({ title: "Passwords do not match", type: "error" });
  } else {
    if (username.length < 5 || password.length < 5) {
      swal({
        title: "Passwords and Username  must be at least 6 characters",
        type: "warning",
      });
    } else {
      handlePostAccount();
    }
  }
}

function PostAccount(data) {
  var api = patch + "api/Accounts/Post";
  fetch(api, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  }).then(function (res) {
    if (res.status == 200) {
      swal("Good job!", "Success", "success");
      setTimeout(() => {
        window.location.assign("./Login.html");
      }, 1000);
    } else {
      swal({ title: "Account does not exist", type: "error" });
    }
  });
}

function handlePostAccount() {
  let username = document.getElementById("username");
  let password = document.getElementById("password");
  let Account = {
    username: username.value,
    password: password.value,
  };
  PostAccount(Account);
}
