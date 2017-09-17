/* global location, WebSocket */
var host = location.origin.replace(/^http/, 'ws');
var client = new WebSocket(host);

var textbox = document.getElementsByTagName('input')[0];
var button = document.getElementsByTagName('button')[0];

client.onmessage = function (message) {
  if (message.data === 'metronomeStart') {
    button.innerHTML = 'End';
    textbox.placeholder = 'Write message';
    (function() {
      var bars = [];
      var initialized = false;
      var height = 0;
      var width = 0;
      var init = function(config) {
        var count = config.count;
        width = config.width;
        height = config.height;
        var center = width / 2;
        var circleMaxWidth = (width * 0.5) >> 0;
        var radius = circleMaxWidth * 0.2;
        var twopi = 2 * Math.PI;
        var change = twopi / count;
        var circlesEl = document.getElementById('circular');
        for (var i = 0; i < twopi; i += change) {
          var node = document.createElement('div');
          node.style.left = (center + radius * Math.cos(i)) + 'px';
          node.style.top = (center + radius * Math.sin(i)) + 'px';
          node.style.webkitTransform = node.style.mozTransform = node.style.transform = 'rotate(' + (i - (Math.PI / 2)) + 'rad)';
          node.style.webkitTransformOrigin = node.style.mozTransformOrigin = node.style.transformOrigin = '0px 0px';
          node.classList.add('circularBar');
          bars.push(node);
          circlesEl.appendChild(node);
        }
        var center = document.createElement('div');
        center.id = 'circularCenter';
        circlesEl.appendChild(center);
        initialized = true;
      };
      var max = 256;
      var renderFrame = function(frequencyData) {
        for (var i = 0; i < bars.length; i++) {
          var bar = bars[i];
          bar.style.height = ((frequencyData[i] / max) * 150) + 'px';
        }
      };
      return {
        init: init,
        isInitialized: function() {
          return initialized;
        },
        renderFrame: renderFrame
      }
    })()
    return
  } else if (message.data === 'metronomeEnd') {
    button.innerHTML = 'Start';
    textbox.placeholder = 'Write message';
    return
  }

  var chatbox = document.getElementById('chatbox');
  var div = document.createElement('div');
  div.className = 'col-xs-12 nopadding';
  div.innerHTML = '<span class="col-xs-11 nopadding">' +
      message.data.replace(/(@\w+)/ig, '<b>$1</b>') +
      '</span><span class="col-xs-1 text-right nopadding">' +
      new Date().toTimeString().split(' ')[0] + '</span>';

  chatbox.appendChild(div);
  chatbox.scrollTop = chatbox.scrollHeight
};

function send () {
  if (!textbox.value) return;

  var message = {
    type: '',
    speed: textbox.value
  };

  if (button.innerHTML === 'Start') {
    message.type = 'metronomeStart'
  } else if (button.innerHTML === 'End') {
    message.type = 'metronomeEnd';
  }

  client.send(JSON.stringify(message));
  textbox.value = '';
}

button.onclick = send;

textbox.onkeypress = function (event) {
  if (event.charCode === 13) send();
};