const tops = document.querySelector('.top')

window.addEventListener('scroll', ()=> {
  const scroll_height = window.pageYOffset
  if (scroll_height > 480 ) {
    tops.classList.add('top-show')
  }
  else {
    tops.classList.remove('top-show')
  }
})
