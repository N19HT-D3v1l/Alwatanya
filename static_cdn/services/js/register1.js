function handleSubmit () {
    const name = document.getElementById('full_name').value;
    const idNum = document.getElementById('id_num').value;

    // to set into local storage
    /* localStorage.setItem("NAME", name);
    localStorage.setItem("SURNAME", surname); */
    // window.location.href = 'register2.html';
    
    sessionStorage.setItem("full_name", name);
    sessionStorage.setItem("id_num", idNum);
    // window.location.replace("register2.html");
    return;
}