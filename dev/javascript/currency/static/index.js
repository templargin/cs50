document.addEventListener('DOMContentLoaded', () => {

  document.querySelector('#form').onsubmit = () => {
    const currency = document.querySelector('#currency').value;
    const request = new XMLHttpRequest();

    request.open('POST', '/convert');

    request.onload = () => {

      const data = JSON.parse(request.responseText);

      if (data.success){
        const contents = `1 EUR equals to ${data.rate} ${currency}`;
        document.querySelector('#result').innerHTML = contents;
      }
      else{
        document.querySelector('#result').innerHTML = 'There was an error.';
      }

    };

    // Add data to send with request
    const data = new FormData();
    data.append('currency', currency);

    // send request
    request.send(data);
    return false;

  };

});
