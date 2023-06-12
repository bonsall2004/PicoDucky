function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("myOverlay").style.display = "block";
}
   
function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById("myOverlay").style.display = "none";
}

function changeFunc() {
  var selectBox = document.getElementById("payloadSelect");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;

  let buttonBox = document.getElementById('buttonBox').innerHTML =`<a href="/run/${selectedValue}"><button type="submit" class="w3-button w3-block w3-padding-large w3-blue w3-margin-bottom">Run Payload</button></a>
  <a href="/edit/${selectedValue}"><button type="submit" class="w3-button w3-block w3-padding-large w3-green w3-margin-bottom">Edit Payload</button></a>
  <a href="/delete/${selectedValue}"><button type="submit" class="w3-button w3-block w3-padding-large w3-red w3-margin-bottom">Delete Payload</button></a>`
  }


function unlockForm() {
  let scriptname = document.getElementById('scriptNameInput')
  if(scriptname.value.length < 0.5) {
    document.getElementById('submitButton').disabled = true;
  } else {
    document.getElementById('submitButton').disabled = false;
  }
}

function checkForm() {
  let ssid = document.getElementById('ssidInputBox').value;
  let password = document.getElementById('passwordInputBox').value;

  if((ssid.length !== 0) & (password.length > 7)) {
    document.getElementById('submit').disabled = false;
  } else {
    document.getElementById('submit').disabled = true;
  }
}

  function goHome() {
    let timeout =  setTimeout(() => {
      window.location.replace('/ducky')
    }, 5000);
    
    console.log(timeout)
    }