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
            .then(response => response.blob())
            .then(blob => {
                // Create a download link
                var url = window.URL.createObjectURL(blob);
                anchor.href = url;
                anchor.download = `${fileId}`;
                anchor.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
    else {
        alert('Select at least one file to download.');
    }
}
