function search() {
    const searchInput = document.getElementById('searchInput').value;

    // Send search request to backend
    fetch(`/search?keyword=${searchInput}`)
        .then(response => response.json())
        .then(data => {
            // Display search results
            const searchResultsDiv = document.getElementById('searchResults');
            searchResultsDiv.innerHTML = '';

            if (data.results.length === 0) {
                searchResultsDiv.innerHTML = 'No results found.';
            } else {
                data.results.forEach(result => {
                    const resultDiv = document.createElement('div');
                    resultDiv.textContent = `Gene Name: ${result.geneName}, Disease Name: ${result.diseaseName}, Z-Score: ${result.zScore}, Confidence Score: ${result.confidenceScore}, URL: ${result.url}`;
                    searchResultsDiv.appendChild(resultDiv);
                });
            }

            // Display statistics
            const statisticsDiv = document.getElementById('statistics');
            statisticsDiv.innerHTML = `Total results: ${data.totalResults}`;
        })
        .catch(error => console.error('Error:', error));
}
