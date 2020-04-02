document.addEventListener('DOMContentLoaded', () => {
  setInterval(count, 300);
});

let counter = 0;
function count(){
  counter++;
  document.querySelector('#counter').innerHTML = counter;
}
