window.onload = Loanding;
var patch = "http://localhost:1994/";

function Loanding() {
  GetAll(handleLoading);
}

function GetAll(callback) {
  var api = patch + "api/History/GetAll";
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

    tdElement1.className = "table__id_history";
    tdElement1.innerHTML = data.id_history;

    tdElement2.className = "table__numberplate";
    tdElement2.innerHTML = data.number_plate;
    tdElement3.innerHTML = `    
        <div class="table__image" style="width: 91px; height: 86px; border: solid 1px rgb(160, 160, 160); border-radius: 4px ">    
        <a href="${data.image}" target="_blank">
        <img src="${data.image}" alt=""
          style=" width: 90px; height :85px; border-radius: 4px ; cursor: pointer;">
        </a>
        </div>   
        `;
    const array = data.time.split("T");
    tdElement4.innerHTML = `
    <div class = "table_date">${array[0]}</div>
    <div class = "table_time">${array[1]}</div>
    `;
    if (data.isout == false) {
      tdElement5.innerHTML = "Go out";
      tdElement5.style = 'color: rgb(217,131,150); font-weight: bold';
    }
    if (data.isout == true) {
      tdElement5.innerHTML = "Go in";
      tdElement5.style = 'color: rgb(93,142,193); font-weight: bold';
    }


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

function on_ModalEdit(id) {
  LoandModalEdit(id);
}

function LoandModalEdit(id) {
  document.getElementById(
    "staticBackdropLabel"
  ).innerHTML = `ID History : ${id}`;
  document.getElementById("bt_Edit").value = id;

  var api1 = patch + "api/Vehicle/GetAll";
  fetch(api1)
    .then((res) => res.json())
    .then((data) => {
      const selectElement = document.getElementById("select");
      selectElement.innerHTML = "";
      data.forEach((item) => {
        const option = document.createElement("option");
        option.value = item.number_plate;
        option.text = item.number_plate;
        option.id = item.number_plate;
        selectElement.appendChild(option);
      });
    });

  var api = patch + `api/History/GetById?id=${id}`;
  fetch(api)
    .then((res) => res.json())
    .then((data) => {
      const array = data.time.split("T");
      document.getElementById("select").value = data.number_plate;
      document.getElementById("datepicker").value = array[0];
      document.getElementById("timepicker").value = array[1];
      if (data.isout == 0) {
        document.getElementById("radio_getInto").checked = false;
        document.getElementById("radio_getOut").checked = true;
      } else {
        document.getElementById("radio_getInto").checked = true;
        document.getElementById("radio_getOut").checked = false;
      }
    });
}

function on_Edit(id_history) {
  var number_plate = document.getElementById("select").value;
  var time = "";
  time += document.getElementById("datepicker").value;
  time += "T";
  time += document.getElementById("timepicker").value;
  var isout;
  if (
    (document.getElementById(`radio_getInto`).value = true
      ? (isout = false)
      : (isout = true))
  );
  let api = patch + "api/History/Put";
  let data = {
    id_history: id_history,
    number_plate: number_plate,
    time: time,
    isout: isout,
  };
  console.log(data);
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
function on_Delete(id) {
  var answer = window.confirm("Delete data?");
  if (answer) {
    var api = patch + `api/History/Delete?id=${id}`;
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

$(function () {
  $("#datepicker").datepicker({
    format: "yyyy-mm-dd",
    autoclose: true,
    orientation: "auto",
    todayHighlight: true,
  });
});

$(function () {
  $("#timepicker").timepicker({
    timeFormat: "hh:mm:ss",
    showMeridian: false,
    icons: {
      up: "fa fa-chevron-up",
      down: "fa fa-chevron-down",
    },
  });
});

document.getElementById("search_id").addEventListener("click", function () {
  var id = document.getElementById("search-input").value;
  if (id.trim() === "") {
    GetAll(handleLoading);
  } else {
    Filter(id, handleLoading);
  }
});

function Filter(id, callback) {
  if (id == "Go in") {
    id = "Go_in";
  }
  if (id == "Go out") {
    id = "Go_out";
  }
  var api = patch + `api/History/Filter?text=${id}`;
  console.log(api);
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
