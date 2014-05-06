RTReversi.Models.Status = Backbone.Model.extend({
    defaults: function () {
        return {
            id: '',
            color: '',
            disc: '',
            board_disc: 0,
            ready: false
        };
    },

    toggleReady: function () {
        this.set('ready', !this.get('ready'));
    }
});
