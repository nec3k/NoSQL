
// Proměnné pro reference na prvky tabulky
var table = document.querySelector('#table-sortable');
var thElements = table.querySelectorAll('th.table-sortable-col');
var tbody = table.querySelector('#table-sortable-body');

// Proměnné pro uchování posledního řazení
var lastSortedCol = 'filename';
var lastSortedOrder = 'asc';

// Kód pro uchování username parametru, pokud existuje a používá se při dotazování API a Generování tabulky
let urlParams = (new URL(document.location)).searchParams;
var usernameParam;
if (urlParams.has("username")){
    usernameParam = `?username=${urlParams.get("username")}`;
} else {
    usernameParam = "";
}

// První načtení dat
//fetchDataAndBuildTable(lastSortedCol, lastSortedOrder);


// Přidání posluchačů událostí pro každé záhlaví tabulky
thElements.forEach(function (th) {
    th.addEventListener('click', function () {
        handleTableHeaderClick(th);
    });
});

// Funkce pro obsluhu kliknutí na záhlaví tabulky
function handleTableHeaderClick(th) {
    var column = th.getAttribute('data-column');
    var order = th.getAttribute('data-order');
    
    // Odstranění tříd pro indikaci řazení na všech th prvcích
    thElements.forEach(th => th.classList.remove('th-sort-asc', 'th-sort-desc'));
    
    // Přidání třídy pro indikaci aktuálního řazení
    th.classList.add(`th-sort-${order}`);

    // Nastaveni atributu data-order pro indikaci přístího řazení
    th.setAttribute('data-order', order === 'desc' ? 'asc' : 'desc');

    // Nastavení dat pro poslední řazení
    lastSortedCol = column;
    lastSortedOrder = order;

    // Znovu načtení dat a sestavení tabulky
    fetchDataAndBuildTable(column, order);
}

// Funkce pro načítání dat z API
function fetchDataAndBuildTable(sortColumn, sortOrder) {
    // Fetch data from API
    fetch(`/api/files${usernameParam}`)
        .then(response => response.json())
        .then(data => {
            // Seřadit data podle sloupce a řádu
            if (sortColumn && sortOrder) {
                data.files.sort((a, b) => compareValues(a[sortColumn], b[sortColumn], sortOrder));
            }

            // Postavit tabulku
            buildTable(data.files);
        });
}

// Funkce pro srovnání hodnot podle typu a směru řazení
function compareValues(a, b, sortOrder) {
    const aValue = typeof a === 'number' ? a : String(a).toLowerCase();
    const bValue = typeof b === 'number' ? b : String(b).toLowerCase();

    // Numerické porovnání, pokud jsou hodnoty čísla
    const numericComparison = typeof aValue === 'number' && typeof bValue === 'number' ? aValue - bValue : 0;

    // Case insensitive porovnání řetězců
    const stringComparison = String(aValue).localeCompare(String(bValue), 'cs', { sensitivity: 'base' });

    // Rozhodnutí podle směru řazení (asc nebo desc)
    return sortOrder === 'asc' ? numericComparison || stringComparison : (numericComparison || stringComparison) * -1;
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
function createTableRow(data, idx) {
    var row = document.createElement('tr');
    row.innerHTML = `
    <td class="px-4 py-1 text-center">
        <input id="id_files_${idx}" type="checkbox" name="files" value="${data.filename}" 
        class="h-8 w-8 rounded border-cyan-950 text-cyan-700 focus:ring-cyan-700">
    </td>            
    <td><label for="id_files_${idx}" class="whitespace-nowrap px-4 py-2 text-cyan-950">
        ${data.filename}
    </label></td>
    <td><p class="whitespace-nowrap px-4 py-2 text-cyan-950">${ (data.size/1024/1024).toFixed(1) } MB</td>
    <td><p class="whitespace-nowrap px-4 py-2 text-cyan-950">${ formatDate(data.ctime*1000) }</td>    
    <td class="whitespace-nowrap px-4 py-1 text-center">
        <div class="flex justify-center">
            <a href="/media/${data.filename}${usernameParam}" download
            class="flex rounded-md bg-cyan-900 px-2 py-1.5 text-white shadow-sm hover:bg-cyan-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-700">
            <svg class="h-6 w-6" fill="none">
                <path d="M17 12L12 17M12 17L7 12M12 17V4M17 20H7" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
            </svg></a>
        </div>
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
    fetchDataAndBuildTable(lastSortedCol, lastSortedOrder);
}
