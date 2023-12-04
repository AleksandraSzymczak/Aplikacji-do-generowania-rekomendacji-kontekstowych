function handleAlgorithmSelection(selectedAlgorithm, selectedFiles) {
    var token = localStorage.getItem('access_token');
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    // Wywołaj funkcję Django za pomocą AJAX
    console.log(selectedAlgorithm);
    console.log(selectedFiles);
    fetch('wybor_algorytmu/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token,
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            algorithm: selectedAlgorithm,
            selected_files: selectedFiles,
        }),
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}