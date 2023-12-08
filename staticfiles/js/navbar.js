document.addEventListener("DOMContentLoaded", function() {
    var submenuParent = document.getElementById('algorithms-info');
    var submenu = submenuParent.querySelector('.submenu');
  
    submenuParent.addEventListener('click', function(event) {
      event.stopPropagation(); // Prevent the click event from reaching the document and closing the submenu
      if (submenu.style.display === 'block') {
        submenu.style.display = 'none';
      } else {
        submenu.style.display = 'block';
      }
    });
  
    // Close the submenu when clicking outside of it
    document.addEventListener('click', function() {
      submenu.style.display = 'none';
    });
  });

  function logoutFunction() {
    console.log("LOGOUT");
    //localStorage.removeItem('access_token');
    //localStorage.removeItem('refresh_token');
    //window.location.href = "/";
    window.location.href = "{% url 'login' %}";

  }