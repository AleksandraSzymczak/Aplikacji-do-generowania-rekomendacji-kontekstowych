function handleAlgorithmSelection(selectedAlgorithm, selectedFiles) {
    //var token = localStorage.getItem('access_token');
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    
    console.log(selectedAlgorithm);
    console.log(selectedFiles);
    if(selectedAlgorithm == "Prefiltering"){
        var redirect_url = "prefiltering/prefiltering_page/"
    }
    if(selectedAlgorithm == "DCR"){
        var redirect_url = "DCR/DCR_page/"
    }
    if(selectedAlgorithm == "DCW"){
        var redirect_url = "DCW/DCW_page/"
    }
    fetch('wybor_algorytmu/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            //'Authorization': 'Bearer ' + token,
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            algorithm: selectedAlgorithm,
            selected_files: selectedFiles[0],
        }),
    })
    .then(response => {
        if (response.ok) {
            window.location.href = redirect_url;
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}
