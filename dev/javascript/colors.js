document.addEventListener('DOMContentLoaded', () => {

  document.querySelectorAll('.color-change').forEach((button, i) => {
    button.onclick = ()=>{
      document.querySelector('#hello').style.color = button.dataset.color;
    };
  });


});
