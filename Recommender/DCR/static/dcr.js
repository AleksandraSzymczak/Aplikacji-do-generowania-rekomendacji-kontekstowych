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
        } else {
            width++;
            progressBar.style.width = width + "%";
            logWindow.innerHTML += "Step " + width + " completed...\n";
        }
    }, 50);
}
