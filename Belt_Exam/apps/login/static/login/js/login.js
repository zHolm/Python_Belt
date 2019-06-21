// input default date as today
$(document).ready(function(){
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() +1;
    var yyyy = today.getFullYear();
    
    if (dd < 10) {
    dd = '0' + dd;
    } 
    if (mm < 10) {
    mm = '0' + mm;
    } 
    var today = yyyy + '-' + mm + '-' + dd;
    document.getElementById('birthday').value = today;
})

//Show login password
function myFunction() {
    var x = document.getElementById("password_login");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
}


//AJAX: validate email uniqueness
$(document).ready(function(){
    $('#email').keyup(function(e){
        e.preventDefault()  // capture all the data in the form in the variable data
        $.ajax({
            method: "GET",   // we are using a post request here, but this could also be done with a get
            url: "/email",
            data: $(this).serialize(),
            success: function(serverResponse){
                $('#emailMsg').html(serverResponse)
            }
        })
        .done(function(res){
            $('#usernameMsg').html(res)
        })  
    })
})





