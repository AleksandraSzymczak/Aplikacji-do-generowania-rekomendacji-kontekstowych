function deleteSelected() {
    var selectedFiles = document.querySelectorAll('.vertical-menu input[type="checkbox"]:checked');
    if (selectedFiles.length > 0) {
        var fileIds = Array.from(selectedFiles).map(checkbox => checkbox.value);
        var token = localStorage.getItem('access_token');
        console.log("Token:", token);
        console.log("File IDs:", fileIds);
        fetch('/data/delete/', {
          method: 'POST',
          headers: {
              "Authorization": "Bearer " + token,
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken
          },
          body: JSON.stringify({ file_ids: fileIds })
      })
      .then(response => {
          console.log("Server Response:", response);
          return response.json();
      })
      .then(data => {
          console.log(data);
          window.location.reload();
      })
      .catch(error => {
          console.error('Error:', error);
      });
    }
}

function downloadSelected() {
var selectedFiles = document.querySelectorAll('.vertical-menu input[type="checkbox"]:checked');

if (selectedFiles.length > 0) {
    var fileIds = Array.from(selectedFiles).map(checkbox => checkbox.value);
    var token = localStorage.getItem('access_token');
    
    console.log("Token:", token);
    console.log("File IDs:", fileIds);

    // Create a hidden anchor element to trigger file downloads
    var anchor = document.createElement('a');
    anchor.style.display = 'none';
    document.body.appendChild(anchor);

    // Fetch files and trigger download
    fileIds.forEach(fileId => {
        fetch(`/data/download/${fileId}/`, {
            method: 'GET',
            headers: {
                "Authorization": "Bearer " + token,
                "X-CSRFToken": csrfToken
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.blob();
        })
        .then(blob => {
            // Create a link element and trigger download
            var a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `file_${fileId}.txt`; // Set the desired filename
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        })
        .catch(error => {
            console.error('Error during file download:', error);
        });
    });
}
else {
    alert('Select at least one file to download.');
}
}
function UploadFile(event) {
    event.preventDefault();

    var token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    var formData = new FormData(document.querySelector('form'));

    fetch("{% url 'upload_file' %}", {
        method: "POST",
        headers: {
            "X-CSRFToken": token,
        },
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            // Handle success
            console.log(data);
        })
        .catch(error => {
            // Handle error
            console.error("There was a problem with the fetch operation:", error);
        });
}