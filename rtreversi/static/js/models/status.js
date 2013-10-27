RTReversi.Models.Status = Backbone.Model.extend({
    default: function () {
        return {
            ready: false,
            name: 'test1'
        };
    },

    toggleReady: function () {
        this.set('ready', !this.get('ready'));
    }
});
