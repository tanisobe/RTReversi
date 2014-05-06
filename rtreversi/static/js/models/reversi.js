RTReversi.Models.Reversi = Backbone.Model.extend({
    defaults: function () {
        return {
            x: 10,
            y: 10,
            size: 10,
            tileLength: 50,
            board: []
        };
    }
});
