window.onload = Loanding;
var patch = "http://localhost:1994/";
max_parked = 6;

function Loanding() {
  Array = ["Vehicle", "History", "Person"];
  count = 0;
  for (let index = 0; index < Array.length; index++) {
    GetNumber(Array[index]);
  }
  console.log(count);

  GetNumberParked();
}

function GetNumberParked() {
  var api = patch + `api/Parking/GetNumberParked`;
  fetch(api)
    .then(function (res) {
      if (res.status == 200) {
        return res.json();
      }
    })
    .then(function (data) {
      document.getElementById("Parking_lot").innerHTML = max_parked - data;
      document.getElementById("Show_Parking_lot").innerHTML = `( ${max_parked - data} / ${max_parked} )`;
    });
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
        document.getElementById("is-out").innerHTML = `(${count} in / ${
          data.length - count
        } out)`;
      }
    });
}
