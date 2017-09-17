'use strict';

var WebSocketServer = require('ws').Server;

module.exports = (server) => {
  var wss = new WebSocketServer({ server: server });

  wss.broadcast = function (data) {
    wss.clients.forEach(function (client) {
      client.send(data)
    })
  };

  wss.on('connection', function (socket) {
    socket.on('message', function (message) {
      try {
        message = JSON.parse(message)
      } catch (e) {
        console.log(e.message)
      }
      console.log(message);
      switch (message.type) {
        case 'metronomeStart':
          socket.username = message.speed;
          socket.send('metronomeStart');
          wss.broadcast('metronomeStart, speed: ' + message.speed);
          break;
        case 'metronomeEnd':
          socket.send('metronomeEnd');
          wss.broadcast('metronomeEnd, speed: ' + message.speed);
          break;
      }
    });

    socket.on('close', function () {
      if (socket.username) {
        wss.broadcast('metronome disconnected');
      }
    })
  })
}