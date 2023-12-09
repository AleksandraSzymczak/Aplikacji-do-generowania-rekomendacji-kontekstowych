document.addEventListener("DOMContentLoaded", function() {
    var submenuParent = document.getElementById('algorithms-info');
    var submenu = submenuParent.querySelector('.submenu');
  
    submenuParent.addEventListener('click', function(event) {
      event.stopPropagation();
      if (submenu.style.display === 'block') {
        submenu.style.display = 'none';
      } else {
        submenu.style.display = 'block';
      }
    });
  
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