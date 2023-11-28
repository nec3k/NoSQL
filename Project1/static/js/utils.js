
// Funkce pro srovnání hodnot podle typu a směru řazení
export function compareValues(a, b, sortOrder) {
    const aValue = typeof a === 'number' ? a : String(a).toLowerCase();
    const bValue = typeof b === 'number' ? b : String(b).toLowerCase();

    // Numerické porovnání, pokud jsou hodnoty čísla
    const numericComparison = typeof aValue === 'number' && typeof bValue === 'number' ? aValue - bValue : 0;

    // Case insensitive porovnání řetězců
    const stringComparison = String(aValue).localeCompare(String(bValue), 'cs', { sensitivity: 'base' });

    // Rozhodnutí podle směru řazení (asc nebo desc)
    return sortOrder === 'asc' ? numericComparison || stringComparison : (numericComparison || stringComparison) * -1;
}

// Načtení dat z url 
export  async function getData(url) {
    try {
        const response = await fetch(url)
        const data = await response.json()
        if (response.status === 200) {
            return data
        } else {
            console.log('Server Error' , data.error.message)
        }
    } catch(error){
        console.log('Fetch Error', error)
    }
}

// Funkce pro formátování data
export  function formatDate(timestamp) {
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

export function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}