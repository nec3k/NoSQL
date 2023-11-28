import { formatDate, compareValues, getData } from "./utils.js";

// Proměnné pro reference na prvky tabulky
var table = document.querySelector('#table-sortable');
var thElements = table.querySelectorAll('th.table-sortable-col');
var tbody = table.querySelector('#table-sortable-body');

// Proměnné pro uchování posledního řazení
var lastSortedCol = 'filename';
var lastSortedOrder = 'asc';

// Kód pro uchování username parametru, pokud existuje a používá se při dotazování API a Generování tabulky
let urlParams = (new URL(document.location)).searchParams;
if (urlParams.has("username")){
    var usernameParam = `?username=${urlParams.get("username")}`;
} else {
    var usernameParam = "";
}
var url = `/api/files${usernameParam}`;

// Prvotní načtení dat
var data;
getData(url).then(new_data =>{
    data = new_data.files;
});

// Přidání posluchačů událostí pro každé záhlaví tabulky
thElements.forEach(function (th) {
    th.addEventListener('click', function () {
        handleTableHeaderClick(th);
    });
});

// Přidání posluchače událostí pro refresh tlačítko
document.querySelector('#refresh-button').addEventListener('click', function() {refresh();});

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
    
    // Seřazení dat a sestavení tabulky
    data.sort((a, b) => compareValues(a[lastSortedCol], b[lastSortedCol], lastSortedOrder));
    buildTable(data);
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
    <td class="px-1 py-1 text-center">
        <input id="id_files_${idx}" type="checkbox" name="files" value="${data.filename}" 
        class="h-8 w-8 rounded border-cyan-950 text-cyan-700 focus:ring-cyan-700">
    </td>            
    <td class="max-w-2xl truncate sm:max-w-sm"><label for="id_files_${idx}" class="whitespace-nowrap px-1 py-2 text-cyan-950">
        ${data.filename}
    </label></td>
    <td><p class="whitespace-nowrap px-1 py-2 text-cyan-950">${ (data.size/1024/1024).toFixed(1) } MB</td>
    <td><p class="whitespace-nowrap px-1 py-2 text-cyan-950">${ formatDate(data.ctime*1000) }</td>    
    <td class="whitespace-nowrap px-1 py-1 text-center">
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

// Funkce pro znovunačtení dat a přegenerování tabulky
function refresh(){
    getData(url).then(new_data =>{
        if (JSON.stringify(data) !== JSON.stringify(new_data.files)){
            data = new_data.files;
            data.sort((a, b) => compareValues(a[lastSortedCol], b[lastSortedCol], lastSortedOrder));
            buildTable(data);
        }
    });
};
