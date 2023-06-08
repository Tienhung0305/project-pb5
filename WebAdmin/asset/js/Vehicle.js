window.onload = Loanding;
const patch = "http://localhost:1994/";

function Loanding() {
  GetAll(handleLoading);
}

function GetAll(callback) {
  var api = patch + "api/Vehicle/GetAll";
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
    let tdElement8 = document.createElement("div");
    let tdElement9 = document.createElement("div");

    tdElement1.innerHTML = data.number_plate;
    tdElement1.className = "mt-2";
    tdElement2.innerHTML = data.car_manufacturer;
    tdElement3.innerHTML = data.name_vehide;
    tdElement4.innerHTML = data.color;
    tdElement5.innerHTML = data.id_person;
    tdElement8.innerHTML = `<button id="bt_edit" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modal_edit" value="${data.number_plate}" onclick="on_ModalEdit('${data.number_plate}')" >Edit</button>`;
    tdElement9.innerHTML = `<button id="bt_delete" type="button" class="btn btn-danger" onclick="on_Delete('${data.number_plate}')" value="${data.number_plate}">Delete</button>`;
    tdElement6.appendChild(tdElement8);
    tdElement7.appendChild(tdElement9);

    trElement.appendChild(tdElement1);
    trElement.appendChild(tdElement2);
    trElement.appendChild(tdElement3);
    trElement.appendChild(tdElement4);
    trElement.appendChild(tdElement5);
    trElement.appendChild(tdElement6);
    trElement.appendChild(tdElement7);

    let tBody = document.getElementById("body");
    tBody.appendChild(trElement);
  }
}

function on_ModalEdit(number_plate) {
  LoandModalEdit(number_plate);
}

function LoandModalEdit(number_plate) {
  document.getElementById(
    "staticBackdropLabel"
  ).innerHTML = `ID Vehicle : ${number_plate}`;
  document.getElementById("bt_Edit").value = number_plate;

  var api = patch + "api/Person/GetAll";
  fetch(api)
    .then((res) => res.json())
    .then((data) => {
      const selectElement = document.getElementById("select");
      selectElement.innerHTML = "";
      data.forEach((item) => {
        const option = document.createElement("option");
        option.value = item.id_person;
        option.text = item.id_person;
        option.id = item.id_person;
        selectElement.appendChild(option);
      });
    });

  var api2 =
    patch + `api/Vehicle/GetByNumberPlate?number_plate=${number_plate}`;
  fetch(api2)
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("input_carManufacturer").value =
        data.car_manufacturer;
      document.getElementById("input_nameVehicle").value = data.name_vehide;
      document.getElementById("input_color").value = data.color;
      document.getElementById(`select`).value = data.id_person;
    });
}

function on_Edit(Number_plate) {
  var Car_manufacturer = document.getElementById("input_carManufacturer").value;
  var Name_vehide = document.getElementById("input_nameVehicle").value;
  var Color = document.getElementById("input_color").value;
  var Id_person = document.getElementById(`select`).value;
  let api = patch + "api/Vehicle/Put";
  let data = {
    number_plate: Number_plate,
    car_manufacturer: Car_manufacturer,
    name_vehide: Name_vehide,
    color: Color,
    id_person: Id_person,
  };
  fetch(api, {
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

function on_Delete(Number_plate) {
  var answer = window.confirm("Delete data?");
  if (answer) {
    var api = patch + `api/Vehicle/Delete?number_plate=${Number_plate}`;
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

function on_LoandModelAdd() {
  var api = patch + "api/Person/GetAll";
  fetch(api)
    .then((res) => res.json())
    .then((data) => {
      const selectElement = document.getElementById("selectAdd");
      selectElement.innerHTML = "";
      data.forEach((item) => {
        const option = document.createElement("option");
        option.value = item.id_person;
        option.text = item.id_person;
        option.id = item.id_person;
        selectElement.appendChild(option);
      });
    });
}

async function on_Add() {
  var id_person = document.getElementById(`selectAdd`).value;
  let check = false;
  const api = patch + `api/Vehicle/CheckByIdProfile?id_profile=${id_person}`;
  const res = await fetch(api);
  const data = await res.json();
  check = Boolean(data);
  if (check == true) {
    var answer = window.confirm("ID profile already exists?");
    if (answer) {
      check = false;
    }
  }

  if (!check) {
    AddVehicle(id_person);
  }
}

function AddVehicle(id_person) {
  var Number_plate = document.getElementById("inputAdd_numberPlate").value;
  var Car_manufacturer = document.getElementById(
    "inputAdd_carManufacturer"
  ).value;
  var Name_vehide = document.getElementById("inputAdd_nameVehicle").value;
  var Color = document.getElementById("inputAdd_color").value;
  var Id_person = id_person;
  let data = {
    number_plate: Number_plate,
    car_manufacturer: Car_manufacturer,
    name_vehide: Name_vehide,
    color: Color,
    id_person: Id_person,
  };
  var api = patch + "api/Vehicle/Post";
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
  var api = patch + `api/Vehicle/Filter?text=${id}`;
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
