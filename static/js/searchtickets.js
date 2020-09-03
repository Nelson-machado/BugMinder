const searchField = document.querySelector("#query")
searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;

    if (searchValue.length > 0) {
        console.log('searchvalue', searchValue);   
    }
})