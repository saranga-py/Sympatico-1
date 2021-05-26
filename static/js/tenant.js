const form = document.querySelector("#form")
const btn1 = document.querySelector('.btn1')
const btn = document.querySelector('.btn')

btn1.addEventListener('click', ()=> {
  form.classList.add('form')
})

btn.addEventListener('click', ()=> {
  btn.classList.toggle('btn--loading')
})
