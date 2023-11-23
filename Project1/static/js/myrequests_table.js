
// Proměnné pro reference na prvky tabulky
var table = document.querySelector('#table-refreshable');
var tbody = table.querySelector('tbody');

// Funkce pro načítání dat z API
function fetchDataAndBuildTable() {
    // Fetch data from API
    fetch(`/api/my_requests`)
        .then(response => response.json())
        .then(data => {
            // Postavit tabulku
            buildTable(data.files);
        });
}

// Funkce pro sestavení tabulky
function buildTable(data) {
    tbody.innerHTML = '';
    document.getElementById('select-all-items').checked = false;

    for (var i = 0; i < data.length; i++) {
        var row = createTableRow(data[i], i);
        tbody.appendChild(row);
    }
}


// Funkce pro vytvoření řádku tabulky
function createTableRow(data) {
    var row = document.createElement('tr');
    row.innerHTML = `
    <td>...
    </td>`;
    return row;
}

// Funkce pro formátování data
function formatDate(timestamp) {
    const months = [
        'ledna', 'února', 'března', 'dubna', 'května', 'června',
        'července', 'srpna', 'září', 'října', 'listopadu', 'prosince'
    ];

    const dateTime = new Date(timestamp);
    const day = dateTime.getDate();
    const month = months[dateTime.getMonth()];
    const year = dateTime.getFullYear();
    const hours = dateTime.getHours();
    const minutes = dateTime.getMinutes();

    return `${day}. ${month} ${year} ${hours}:${minutes < 10 ? '0' : ''}${minutes}`;
}

// Funkce pro znovunačtení dat a přegenerování tabulky
function refreshData(){
    fetchDataAndBuildTable();
}
