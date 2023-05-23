window.onload = Loanding;
var patch = "http://localhost:1994/";

function Loanding() {
  Array = ["Vehicle", "History", "Person"];
  count = 0;
  for (let index = 0; index < Array.length; index++) {
    GetNumber(Array[index]);
  }
  console.log(count);
}

function GetNumber(string) {
  var api = patch + `api/${string}/GetAll`;
  fetch(api)
    .then(function (res) {
      if (res.status == 200) {
        return res.json();
      }
    })
    .then(function (data) {
      document.getElementById(string).innerHTML = data.length;
      if (string == "History") {
        for (let index = 0; index < data.length; index++) {
          data[index].isout == true ? count++ : count;
        }
        document.getElementById("is-out").innerHTML = `(${data.length-count} in/ ${count} out)`;
      }
    });
}
