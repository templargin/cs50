document.addEventListener('DOMContentLoaded', () => {

  console.log("TESTING");

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  socket.on('connect', () => {
    console.log("socket connect");

    document.querySelectorAll('button').forEach(button => {
      button.onclick = () => {
        const selection = button.dataset.vote;
        socket.emit('submit vote', {'votemarker':selection});
      };
    });
  });

  socket.on('vote results', data => {
    console.log("socket results");
    document.querySelector('#yes').innerHTML = data.yes;
    document.querySelector('#no').innerHTML = data.no;
    document.querySelector('#maybe').innerHTML = data.hz;
  });

});
