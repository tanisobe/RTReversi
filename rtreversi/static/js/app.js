RTReversi.App = Backbone.View.extend({
    el: '#app',
    initialize: function () {
        RTReversi.EventDispatcher = {};
        _.extend(RTReversi.EventDispatcher, Backbone.Events);

        this.reversi = new RTReversi.Views.Reversi({
            el: '#game',
            model: new RTReversi.Models.Reversi()
        });

        this.status = new RTReversi.Views.StatusCollection({
            el: '#status',
            collection: new RTReversi.Collections.Status()
        });

        this.communicator = new RTReversi.Views.Communicator();
    }
});

new RTReversi.App();
