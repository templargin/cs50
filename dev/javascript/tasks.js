document.addEventListener('DOMContentLoaded', () => {

  document.querySelector('#submit').disabled = true;

  document.querySelector('#task').onkeyup = () => {
    if (document.querySelector('#task').value.length > 0){
      document.querySelector('#submit').disabled = false;
    }
    else {
      document.querySelector('#submit').disabled = true;
    }
  };

  document.querySelector('#new-task').onsubmit = () => {

    const li = document.createElement('li');
    li.innerHTML = document.querySelector('#task').value;

    document.querySelector('#tasks').append(li);

    document.querySelector('#task').value = '';
    document.querySelector('#submit').disabled = true;

    return false;
  };

});
