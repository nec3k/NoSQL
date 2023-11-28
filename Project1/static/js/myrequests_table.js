import { formatDate, getData, capitalizeFirstLetter } from "./utils.js";

// Proměnné pro reference na prvky tabulky
var table = document.querySelector('#table-refreshable');
var tbody = table.querySelector('#table-refreshable-body');

// Kód pro uchování username parametru, pokud existuje a používá se při dotazování API a Generování tabulky
let urlParams = (new URL(document.location)).searchParams;
if (urlParams.has("page")){
    var pageParam = `?page=${urlParams.get("page")}`;
} else {
    var pageParam = "";
}
var url = `/api/my_requests${pageParam}`;

// Přidání posluchače událostí pro refresh tlačítko
document.querySelector('#refresh-button').addEventListener('click', function() {refresh();});

// Funkce pro sestavení tabulky
function buildTable(data) {
    tbody.innerHTML = '';

    for (var i = 0; i < data.length; i++) {
        var row = createTableRow(data[i]);
        tbody.appendChild(row);
    }
}


// Funkce pro vytvoření řádku tabulky
function createTableRow(data) {
    var row = document.createElement('tr');
    row.innerHTML = `
    <tr>
      <td> <p class="badge-${ data.task__status.toLowerCase() } text-center">${data.task__status }</p></td>
      <td> <p class="whitespace-nowrap px-1 py-2 text-cyan-950 text-center">${ capitalizeFirstLetter(data.format__file_type) }</p></td>
      <td> <p class="whitespace-nowrap px-1 py-2 text-cyan-950 text-center">${ formatDate(data.task__date_created*1000) }</p></td>
      <td class="max-w-xl sm:max-w-sm "> <p class="whitespace-nowrap px-1 py-2 text-cyan-950 truncate">${ data.downloaded_files.join(", ")}</p></td>
      <td class="text-center"> <a href="${ data.url }" class="whitespace-nowrap px-1 py-2 text-cyan-700 underline" target="_blank">Odkaz</a></td>
    </tr>
    `;
    return row;
}

// Funkce pro znovunačtení dat a přegenerování tabulky
function refresh(){
    getData(url).then(new_data =>{
        if (JSON.stringify(data) !== JSON.stringify(new_data.my_requests)){
            var data = new_data.my_requests;
            buildTable(data);    
        }
    });
};
