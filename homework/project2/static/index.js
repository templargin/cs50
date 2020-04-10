$(function() {

  var socket=io.connect(location.protocol+'//'+document.domain+':'+location.port);

  // localStorage.clear();

  // Listening to "connect" socket
  socket.on('connect', () => {
    if (!localStorage.getItem('displayName')){
      $('#myModal').modal({backdrop: 'static', keyboard: false});
      $("#modalSubmit").attr('disabled',true);
      $('.modal-title').text("Choose your display name.");
    }
  });

  // load all channels
  // broadcasting to everyone
  socket.on('load channels', data => {
    $('#channelList li').remove();
    loadChannels(data);
    $('#'+localStorage.getItem('activeChannel')).click();
  });

  // Open up a window for submitting a channel
  $('#btnAddChannel').on('click', function() {
    $('#myModal').modal({keyboard: true, show: true});
    $('#modalInput').val("");
    $('#modalInput').focus();
    $('.modal-title').text("Choose channel name.");
  });


  // Sending "modalSubmit" to server
  // Submitting a new channel or new username
  $('#modalSubmit').on('click', function() {
    if (!localStorage.getItem('displayName')){
      var username = $('#modalInput').val();
      socket.emit('username submitted', {'username':username});
    }
    else{
      var channel_name = $('#modalInput').val();
      channel_name = channel_name.toLowerCase();
      var user = localStorage.getItem('displayName');
      socket.emit('channel submitted', {'channel_name':channel_name, 'user':user});
    }
  });

  // Receiving "add username" from server
  socket.on('add username', data => {
    if (data["success"]){
      // set a display name
      localStorage.setItem('displayName', data["username"]);
      $('#username').text(localStorage.getItem('displayName'));

      // hide modal
      $('#myModal').modal('hide');


      // set general as an active channel
      activeChannel = "general";
      localStorage.setItem('activeChannel', activeChannel);
      $('#'+localStorage.getItem('activeChannel')).click();

    }
    else{
      $('#myModal').modal({backdrop: 'static', keyboard: false, show: true});
      $('#modalInput').val("");
      $('#modalInput').focus();
      $("#modalSubmit").attr('disabled',true);
      $('.modal-title').text("This username already exists. Try another one.");
    }
  });

  // Receiving "add channel" from server
  socket.on('update channels', data => {
    if (data["success"]){

      // add channel for everyone
      channel = data["channel_name"];
      appendChannel(channel);
      $('#myModal').modal('hide');

      // redirect the user who added channel to new channel
      if (data["user"] === localStorage.getItem('displayName')){
        localStorage.setItem('activeChannel', data["channel_name"]);
        $('#'+localStorage.getItem('activeChannel')).click();
      }

    }
    else{
      if (data["user"] === localStorage.getItem('displayName')){
        $('#myModal').modal({keyboard: true, show: true});
        $('#modalInput').val("");
        $('#modalInput').focus();
        $("#modalSubmit").attr('disabled',true);
        $('.modal-title').text("This channel already exists. Try another one.");
      }
    }
  });

  // Selecting a channel
  // Switching between one to another
  $('#channelList').on('click', 'li', function() {
      $(this).addClass('active');
      $(this).siblings().removeClass('active');

      var activeChannel = $("#channelList .active").attr('id');
      localStorage.setItem('activeChannel', activeChannel);

      socket.emit('channel selected', {'activeChannel': activeChannel});
  });

  // Showing channel's content
  socket.on('show channel', data => {
    $('#messages div').remove();
    showChannel(data);
    $('#messageInput').focus();
  });

  // Sending a message
  $('#btnSubmitMessage').on('click', function() {
    const text = $('#messageInput').val();
    const time =new Date().toLocaleString();
    const user=localStorage.getItem('displayName');

    var activeChannel = localStorage.getItem('activeChannel');

    socket.emit('message sent', {'text': text,'time':time, 'user':user,'channel':activeChannel});

    $('#messageInput').val("");
    $('#messageInput').focus();
  });

  // Send a message with "Enter"
  $("#messageInput").on('keyup', function (key) {
    if (key.keyCode==13 ) {
        $('#btnSubmitMessage').click();
    }
  });

  // Showing a message only if the same channel
  socket.on('add message', data => {
    if (data["channel"] === localStorage.getItem('activeChannel')){
      appendMessage(data);
    }
  });

  // Display username
  $('#username').text(localStorage.getItem('displayName'));


  // INPUT CONTROLS
  $("#modalInput").on('click', function (){
    $("#modalSubmit").attr('disabled',true);
  });

  $("#modalInput").on('keypress', function (key){
    if (localStorage.getItem('displayName')){
      var inputRGEX = /^[a-zA-Z]*$/;
    }
    else{
      var inputRGEX = /^[a-zA-Z0-9]*$/;
    }
    var inputResult = inputRGEX.test(key.key);
    if(!(inputResult)){
      return false;
    }
  });

  $("#modalInput").on('keyup', function (key) {

    if ( $(this).val().length > 0 ){
        $("#modalSubmit").attr('disabled',false);
        if (key.keyCode==13 ) {
            $('#modalSubmit').click();
        }
    }
    else {
        $("#modalSubmit").attr('disabled',true);
    }
  });

});


function loadChannels(data){
  for (channel in data){
    appendChannel(channel);
  }
}

function appendChannel(channel){
  const li = document.createElement('li');
  li.innerHTML = '# ' + channel;
  //li.className = "list-group-item";
  li.setAttribute("id", channel);
  //li.setAttribute("class", 'list-group-item');
  $('#channelList').append(li);
}


function showChannel(data){
  var currentChannel = localStorage.getItem('activeChannel');
  var welcomeText = "#" + currentChannel;
  $('#channelHeader').text(welcomeText);
  for (i in data){
    appendMessage(data[i]);
  }
}

function appendMessage(message){
  const message_box = document.createElement('div');

  const username = document.createElement('span');
  username.innerHTML = message["user"];
  username.className='text-primary';

  const text = document.createElement('p');
  text.innerHTML = message["text"];

  const time=document.createElement('small');
  time.innerHTML=message["time"];
  time.className='text-muted pl-2';

  message_box.append(username);
  message_box.append(time);
  message_box.append(text);

  $('#messages').append(message_box);
  $('#messages').scrollTop(10000);
}
