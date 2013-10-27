RTReversi.Views.Status = Backbone.View.extend({
    tagName: 'li',
    template: _.template('hoge'),

    initialize: function () {
        this.$el.html(this.template());
    },

    render: function() {
        this.$el.html(this.template());
    }
});
