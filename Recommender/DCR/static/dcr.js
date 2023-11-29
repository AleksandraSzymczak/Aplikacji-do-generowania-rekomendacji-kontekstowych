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
  function startProcess() {
    var progressBar = document.getElementById("myBar");
    var progressContainer = document.getElementById("progressContainer");
    var reportContent = document.getElementById("reportContent");
    var logWindow = document.getElementById("logWindow");

    progressBar.style.width = "0%";
    logWindow.innerHTML = "";

    progressContainer.style.display = "block";

    logWindow.innerHTML += "Processing started...\n";

    var width = 0;
    var interval = setInterval(function () {
        if (width >= 100) {
            clearInterval(interval);
            logWindow.innerHTML += "Processing completed.\n";
            reportContent.style.display = "block";
        } else {
            width++;
            progressBar.style.width = width + "%";
            logWindow.innerHTML += "Step " + width + " completed...\n";
        }
    }, 50);
}
function updateSliderValue(slider, context_var) {
  var output = document.getElementById("value_" + context_var);
  output.innerHTML = slider.value;

  var hiddenValuesField = document.getElementById('hidden_values');
  var hiddenValues = JSON.parse(hiddenValuesField.value || '{}');
  hiddenValues[context_var] = slider.value;
  hiddenValuesField.value = JSON.stringify(hiddenValues);
}
