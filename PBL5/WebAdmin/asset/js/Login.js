function onLogin() {
  GetAccounts(hanldeLogin);
}
const patch = "http://localhost:1994/";

function GetAccounts(callback) {
  var api = patch + "api/Accounts/GetAll";
  fetch(api)
    .then(function (res) {
      if (res.status == 200) {
        return res.json();
      } else {
        wal({ title: "Error", type: "error" });
      }
    })
    .then(callback);
}

function hanldeLogin(data) {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  console.log(data, username, password);
  var Check = false;
  if (username == "" || password == "") {
    swal({ title: "Please enter your username and password", type: "error" });
  } else {
    data.forEach((data) => {
      if (data.username == username && data.password == password) {
        Check = true;
      }
    });
    if (Check == true) {
      swal({ title: "Success", type: "success" });
      setTimeout(() => {
        window.location.assign("./Dashboard.html");
      }, 1000);
    } else {
      swal({ title: "The username or password is incorrect", type: "error" });
    }
  }
}
