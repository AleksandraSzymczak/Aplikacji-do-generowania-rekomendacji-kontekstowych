function handleAlgorithmSelection(selectedAlgorithm, selectedFiles) {
    //var token = localStorage.getItem('access_token');
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    
    console.log(selectedAlgorithm);
    console.log(selectedFiles);
    if(selectedAlgorithm == "collaborative_filtering"){
        var redirect_url = "collaborative_filtering/collaborative_filtering_page/"
    }
    if(selectedAlgorithm == "exact_prefiltering"){
        var redirect_url = "exact_prefiltering/exact_prefiltering_page/"
    }
    if(selectedAlgorithm == "DCR"){
        var redirect_url = "DCR/DCR_page/"
    }
    fetch('wybor_algorytmu/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
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
