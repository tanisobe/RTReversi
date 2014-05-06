RTReversi.Views.Communicator = Backbone.View.extend({
    initialize: function() {
        _.bindAll(this, 'putDisc', 'removeDisc', 'changeStatus');
        RTReversi.EventDispatcher.on('putDisc', this.putDisc);
        RTReversi.EventDispatcher.on('removeDisc', this.removeDisc);
        RTReversi.EventDispatcher.on('changeStatus', this.changeStatus);
        var url = 'ws://' + '192.168.0.7:5000' + '/reversi';
        this.socket = new WebSocket(url);
        this.socket.onmessage = this.onMessage;
    },

    putDisc: function (param) {
        j = {
            'command': 'putDisc',
            'param': param
        };
        this.socket.send(JSON.stringify(j));
    },

    removeDisc: function (param) {
        j = {
            'command': 'removeDisc',
            'param': param
        };
        this.socket.send(JSON.stringify(j));
    },

    changeStatus: function (param) {
        j = {
            'command': 'changeStatus',
            'param': param
        };
        console.log(j);
        this.socket.send(JSON.stringify(j));
    },

    onMessage: function (evt) {
        msg = JSON.parse(evt.data);
        switch (msg.command){
            case 'updateGame':
            RTReversi.EventDispatcher.trigger('updateReversi', msg.param.board);
            RTReversi.EventDispatcher.trigger('updatePlayerStatus', msg.param.players);
            break;
        }
    }
});
