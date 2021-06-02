var date = new Date()
document.getElementById('date').innerHTML = date.getFullYear()

const profile = document.querySelector('.profile')
const user = document.querySelector('.login')

window.addEventListener('scroll', ()=> {
  profile.classList.remove('show-profile')
})

user.addEventListener('click', ()=> {
  profile.classList.toggle('show-profile')
})

const alert = document.querySelector(".alert")

alert.addEventListener('click', ()=> {
  alert.classList.add("alerts")
})

function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
