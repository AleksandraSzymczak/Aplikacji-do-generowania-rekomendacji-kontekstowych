document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();

    var formData = new FormData(this);
    
    //var token = localStorage.getItem('access_token');

    fetch("{% url 'upload_file' %}", {
      method: 'POST',
      body: formData,
      //headers: {
      //  'Authorization': 'Bearer ' + token,
      //},
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('File uploaded successfully!');
      } else {
        alert('Error uploading file. Please try again.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });