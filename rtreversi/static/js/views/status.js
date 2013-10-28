RTReversi.Views.Status = Backbone.View.extend({
    tagName: 'li',
    template: _.template('id: <%= id %>, disc: <%=disc %>, color: <%=color %>'),

    initialize: function () {
        _.bindAll(this, 'render');
        RTReversi.EventDispatcher.on('renderPlayerStatus', this.render);
    },

    render: function() {
        var tmpl = this.template(this.model.toJSON());
        return this.$el.html(tmpl);
    }
});
