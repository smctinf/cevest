let btnMobile = document.querySelector('.menuMobile')
let divMobile = document.querySelector('.menuMobile-div')
let aberto = false
const btnGira = () => {
  if(aberto == false){
    divMobile.classList.add('divMobileAberta')
    aberto = true
  }
  else{
    divMobile.classList.remove('divMobileAberta')
    aberto = false
  }
}
btnMobile.addEventListener('click', btnGira)