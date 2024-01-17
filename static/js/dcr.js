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
  var mse = document.getElementById("mseResult");
  var KFold = document.getElementById("KFold");
  var yesOption = document.getElementById("yes").checked;
  var minValue = 0;
  var maxValue = 0;

  if (yesOption) {
    minValue = document.getElementById("min").value;
    maxValue = document.getElementById("max").value;
  }

  var radioButtons = document.getElementsByName("data_cleanup");

  var selectedOption;
  for (var i = 0; i < radioButtons.length; i++) {
    if (radioButtons[i].checked) {
      selectedOption = radioButtons[i].value;
      break;
    }
  }

  var zscoreYes = document.getElementById("Zscore_yes");
  var zscoreNo = document.getElementById("Zscore_no");
  var shouldUseZscore;

  if (zscoreYes.checked) {
    shouldUseZscore = true;
  } else if (zscoreNo.checked) {
    shouldUseZscore = false;
  } else {
    shouldUseZscore = null;
  }
  progressBar.style.width = "0%";
  logWindow.innerHTML = "";

  progressContainer.style.display = "block";

  logWindow.innerHTML += "Processing started...\n";
  var selectedFile = document.getElementById("fileCont").dataset.file;
  startLogUpdates();
  callAjaxFunction(selectedFile, KFold.value, maxValue, minValue, selectedOption, shouldUseZscore).then(function (data) {
    var result = JSON.stringify(data);
    var parsedResult = JSON.parse(result);
    var resData = parsedResult.data;
    console.log(resData.mse)
    if ('mae' in resData) {
      mae.textContent = "MAE: " + resData.mae;
    }
    if ('rmse' in resData) {
      rmse.textContent = "RMSE: " + resData.rmse;
    }
    if ('mse' in resData) {
      mse.textContent = "MSE: " + resData.mse;
    }
    reportContent.style.display = "block";
    logWindow.innerHTML += "Processing ended...\n";
  });
}


function startLogUpdates() {
  var logWindow = document.getElementById("logWindow");

  // Tworzymy nowy obiekt EventSource do nasłuchiwania na zmiany w pliku log.txt
  const eventSource = new EventSource(`/mainpage/collaborative_filtering/collaborative_filtering_page/Wyniki_collaborative_filtering/log-stream/`);

  // Obsługa zdarzenia (nowa linia w logu)
  eventSource.onmessage = function (event) {
    const logLine = event.data;
    logWindow.innerHTML += logLine + "<br>";
  };

  // Obsługa zamknięcia po zakończeniu procesu
  eventSource.onclose = function () {
    logWindow.innerHTML += "Processing ended...\n";
  };
}


function callAjaxFunction(selectedFile, KFold, maxValue, minValue, selectedOption, shouldUseZscore) {
  return new Promise(function (resolve, reject) {
    $.ajax({
      url: `/mainpage/collaborative_filtering/collaborative_filtering_page/Wyniki_collaborative_filtering/simulate_long_running_process/${selectedFile}/`,
      type: "GET",
      dataType: "json",
      data: { 
        file: selectedFile, 
        KFold: KFold,
        maxValue: maxValue,
        minValue: minValue,
        cleanup_data: selectedOption,
        Zscore: shouldUseZscore
      }, 
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
  var hiddenValuesField = document.getElementById('hidden_values');
  
  // Jeśli wartość suwaka jest mniejsza niż 2, ustaw na 2
  if (slider.value < 2) {
    slider.value = 2;
  }

  output.innerHTML = slider.value;

  var hiddenValues = JSON.parse(hiddenValuesField.value || '{}');
  hiddenValues[context_var] = slider.value;
  hiddenValuesField.value = JSON.stringify(hiddenValues);
}


function displayHistogram(estimatedValues) {
  var ctx = document.getElementById('myChart').getContext('2d');

  var histogramChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: estimatedValues.map((_, index) => index + 1),
      datasets: [{
        label: 'Histogram of Estimated Values',
        data: estimatedValues,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        x: {
          type: 'linear',
          position: 'bottom'
        }
      }
    }
  });
}

// Call the function to display the histogram
displayHistogram(estimated_values);

// Create a function to display the scatter plot
function displayScatterPlot(actualRatings, estimatedRatings) {
  var ctx = document.getElementById('myChart').getContext('2d');

  var scatterPlot = new Chart(ctx, {
    type: 'scatter',
    data: {
      labels: uids_iids.map((uid_iid) => `${uid_iid[0]}, ${uid_iid[1]}`),
      datasets: [{
        label: 'Actual Ratings',
        data: actualRatings,
        backgroundColor: 'red',
        pointRadius: 5,
        showLine: false
      }, {
        label: 'Estimated Ratings',
        data: estimatedRatings,
        backgroundColor: 'green',
        pointRadius: 5,
        showLine: false
      }]
    },
    options: {
      scales: {
        x: {
          type: 'linear',
          position: 'bottom'
        },
        y: {
          min: Math.min(...actualRatings, ...estimatedRatings),
          max: Math.max(...actualRatings, ...estimatedRatings),
        }
      }
    }
  });
}

// Call the function to display the scatter plot
displayScatterPlot(actual_ratings, estimated_ratings);