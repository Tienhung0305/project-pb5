window.onload = Loanding;
var patch = "http://localhost:1994/";

function Loanding() {
  GetAll(handleLoading);
}

function GetAll(callback) {
  var api = patch + "api/Person/GetAll";
  fetch(api)
    .then(function (res) {
      if (res.status == 200) {
        return res.json();
      }
    })
    .then(callback);
}

function handleLoading(data) {
  var body = document.getElementById("body");
  while (body.firstChild) {
    body.removeChild(body.firstChild);
  }
  if (Array.isArray(data)) {
    data.forEach((data) => {
      AddTable(data);
    });
  } else {
    AddTable(data);
  }
}

function AddTable(data) {
  if (data != null) {
    let trElement = document.createElement("tr");
    let tdElement1 = document.createElement("td");
    let tdElement2 = document.createElement("td");
    let tdElement3 = document.createElement("td");
    let tdElement4 = document.createElement("td");
    let tdElement5 = document.createElement("td");
    let tdElement6 = document.createElement("td");
    let tdElement7 = document.createElement("td");
    let tdElement10 = document.createElement("td");
    let tdElement8 = document.createElement("div");
    let tdElement9 = document.createElement("div");

    tdElement1.innerHTML = data.id_person;
    tdElement1.className = "mt-2";
    tdElement2.innerHTML = data.name;
    tdElement3.innerHTML = data.gender;
    tdElement4.innerHTML = data.phoneNumber;
    tdElement5.innerHTML = data.email;

    if (data.active == true) {
      tdElement10.innerHTML = `
      <div class="container">
      <input type="checkbox" class="checkActive" id="checkActive_${data.id_person}" onclick="putActive(${data.id_person}, this.checked)" checked>
      <label for="checkActive_${data.id_person}" class="button"></label>
    </div>`
    } else {
      tdElement10.innerHTML = `
      <div class="container">
      <input type="checkbox" class="checkActive" id="checkActive_${data.id_person}" onclick="putActive(${data.id_person}, this.checked)" >
      <label for="checkActive_${data.id_person}" class="button"></label>
    </div>`
    }

    tdElement8.innerHTML = `<button id="bt_edit" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modal_edit" value="${data.id_person}" onclick="on_ModalEdit(${data.id_person})" >Edit</button>`;
    tdElement9.innerHTML = `<button id="bt_delete" type="button" class="btn btn-danger" onclick="on_Delete(${data.id_person})" value="${data.id_person}">Delete</button>`;
    tdElement6.appendChild(tdElement8);
    tdElement7.appendChild(tdElement9);
    trElement.appendChild(tdElement1);
    trElement.appendChild(tdElement2);
    trElement.appendChild(tdElement3);
    trElement.appendChild(tdElement4);
    trElement.appendChild(tdElement5);
    trElement.appendChild(tdElement10);
    trElement.appendChild(tdElement6);
    trElement.appendChild(tdElement7);

    let tBody = document.getElementById("body");
    tBody.appendChild(trElement);
  }
}

function on_ModalEdit(id) {
  LoandModalEdit(id);
}

function LoandModalEdit(id) {
  document.getElementById(
    "staticBackdropLabel"
  ).innerHTML = `ID Profile : ${id}`;
  document.getElementById("bt_Edit").value = id;
  var api = patch + `api/Person/GetById?id=${id}`;
  fetch(api)
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("input_name").value = data.name;
      document.getElementById("input_phonenumber").value = data.phoneNumber;
      document.getElementById("input_email").value = data.email;
      console.log(data);
      if (data.gender == "Nam") {
        document.getElementById("radio_Nam").checked = true;
        document.getElementById("radio_Nu").checked = false;
      } else {
        document.getElementById("radio_Nam").checked = false;
        document.getElementById("radio_Nu").checked = true;
      }
    });
}

function putActive(id,active) {
    let api = patch + `api/Person/PutActive?id=${id}&active=${active}`;
    fetch(api, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },

    }).then(function (res) {
      if (res.status != 200) {
        swal({ title: "error", type: "error" });
      }
    });
}

function on_Edit(id) {
  var name = document.getElementById("input_name").value;
  var phone = document.getElementById("input_phonenumber").value;
  var email = document.getElementById("input_email").value;
  var active = document.getElementById(`checkActive_${id}`).checked;

  if (document.getElementById("radio_Nam").checked == true) {
    var gender = "Nam";
  } else {
    var gender = "Nữ";
  }
  let apiUser = patch + "api/Person/Put";
  let data = {
    id_person: id,
    active: active,
    name: name,
    gender: gender,
    phoneNumber: phone,
    email: email,
  };
  console.log(data);

  fetch(apiUser, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  }).then(function (res) {
    if (res.status == 200) {
      swal({ title: "Success", type: "success" });
      setTimeout(() => {
        location.reload();
      }, 1000);
    } else {
      swal({ title: "error", type: "error" });
    }
  });
}

function on_Delete(id) {
  var answer = window.confirm("Delete data?");
  if (answer) {
    var api = patch + `api/Person/Delete?id=${id}`;
    fetch(api, {
      method: "DELETE",
    }).then(function (res) {
      if (res.status == 200) {
        swal({ title: "Success", type: "success" });
        setTimeout(() => {
          location.reload();
        }, 1000);
      } else {
        swal({ title: "error", type: "error" });
      }
    });
  }
}

function on_Add() {
  var name = document.getElementById("inputAdd_name").value;
  var phone = document.getElementById("inputAdd_phonenumber").value;
  var email = document.getElementById("inputAdd_email").value;
  if (document.getElementById("radioAdd_Nam").checked == true) {
    var gender = "Nam";
  } else {
    var gender = "Nữ";
  }
  let data = {
    active: true,
    name: name,
    gender: gender,
    phoneNumber: phone,
    email: email,
  };
  var api = patch + "api/Person/Post";
  fetch(api, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  }).then(function (res) {
    if (res.status == 200) {
      swal({ title: "Success", type: "success" });
      setTimeout(() => {
        location.reload();
      }, 1000);
    } else {
      swal({ title: "Error", type: "error" });
    }
  });
}

document.getElementById("search_id").addEventListener("click", function () {
  var id = document.getElementById("search-input").value;
  if (id === "") {
    GetAll(handleLoading);
  } else {
    Filter(id, handleLoading);
  }
});

function Filter(id, callback) {
  var api = patch + `api/Person/Filter?text=${id}`;
  fetch(api)
    .then(function (res) {
      if (res.status == 200) {
        return res.json();
      } else {
        return null;
      }
    })
    .then(callback);
}
