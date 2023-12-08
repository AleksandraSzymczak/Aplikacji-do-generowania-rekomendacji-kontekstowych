document.addEventListener('DOMContentLoaded', function() {
  var checkboxes = document.querySelectorAll('input[type="checkbox"]');

  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
      var checkboxName = this.name;
      var checkboxValue = this.value;

      checkboxes.forEach(function(otherCheckbox) {
        if (
          otherCheckbox !== checkbox &&
          otherCheckbox.name !== checkboxName &&
          otherCheckbox.value === checkboxValue
        ) {
          otherCheckbox.checked = false;
          otherCheckbox.disabled = checkbox.checked;
        }
      });
    });
  });
});

function getJwtToken() {
  return localStorage.getItem('access_token');
}

function startProcess() {
  var progressBar = document.getElementById("myBar");
  var progressContainer = document.getElementById("progressContainer");
  var reportContent = document.getElementById("reportContent");
  var logWindow = document.getElementById("logWindow");
  var mae = document.getElementById("maeResult");
  var rmse = document.getElementById("rmseResult");
  var recall = document.getElementById("recallResult");


  progressBar.style.width = "0%";
  logWindow.innerHTML = "";

  progressContainer.style.display = "block";

  logWindow.innerHTML += "Processing started...\n";
  var selectedFile = document.getElementById("fileCont").dataset.file;

  callAjaxFunction(selectedFile).then(function (data) {
    var result = JSON.stringify(data);
    var parsedResult = JSON.parse(result);
    var resData = parsedResult.data;
    if ('mae' in resData) {
      mae.textContent = "MAE: " + resData.mae;
    }
    if ('rmse' in resData) {
      rmse.textContent = "RMSE: " + resData.rmse;
    }
    if ('recall_result' in resData) {
      recall.textContent = "Recall Result: " + resData.recall_result;
    }
    reportContent.style.display = "block";
    logWindow.innerHTML += "Processing ended...\n";
  });
}

function callAjaxFunction(selectedFile) {
  return new Promise(function (resolve, reject) {
    $.ajax({
      url: `/mainpage/prefiltering/prefiltering_page/Wyniki_prefiltering/simulate_long_running_process/${selectedFile}/`,
      type: "GET",
      dataType: "json",
      data: { file: selectedFile }, 
      //headers: {
        //"Authorization": "Bearer " + getJwtToken(),
      //},
      success: function (data) {
        resolve(data);
      },
      error: function (error) {
        reject(error);
      },
    });
  });
}

function updateSliderValue(slider, context_var) {
  var output = document.getElementById("value_" + context_var);
  output.innerHTML = slider.value;

  var hiddenValuesField = document.getElementById('hidden_values');
  var hiddenValues = JSON.parse(hiddenValuesField.value || '{}');
  hiddenValues[context_var] = slider.value;
  hiddenValuesField.value = JSON.stringify(hiddenValues);
}
