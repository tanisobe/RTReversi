RTReversi.Models.Status = Backbone.Model.extend({
    default: function () {
        return {
            ready: false,
            id: '',
            color: '',
            disc: ''
        };
    },

    toggleReady: function () {
        this.set('ready', !this.get('ready'));
    }
});
