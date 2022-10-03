let privileges = document.getElementsByClassName('textbox');
let makeChangesButton = document.getElementsByClassName('make-changes')[0];
makeChangesButton.addEventListener('click', async evt => {
    let privilegeArray = [];
    
    for (let privilege of privileges) {
        if (privilege.value !== privilege.placeholder) {
            privilegeArray.push({
                id: privilege.name,
                value: privilege.value,
            });
        }
    }
    let parameters = {
        method: "POST",
        body: JSON.stringify(privilegeArray),
    }
    let response = await fetch("/admin", parameters);
    console.log(await response.json());
});