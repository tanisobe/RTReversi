RTReversi.App = Backbone.View.extend({
    el: '#app',
    initialize: function () {
        RTReversi.EventDispatcher = {};
        _.extend(RTReversi.EventDispatcher, Backbone.Events);

        this.reversi = new RTReversi.Views.Reversi({
            el: '#game',
            model: new RTReversi.Models.Reversi({x: 8, y: 8, size: 8, tileLength: 60})
        });

        this.status = new RTReversi.Views.Status({
            el: '#status'
        });

        this.communicator = new RTReversi.Views.Communicator();
    }
});

new RTReversi.App();
