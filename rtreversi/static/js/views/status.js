RTReversi.Views.Status = Backbone.View.extend({
    tagName: 'li',
    className: 'statusPanel',
    template: _.template( "\
        <div>ready: <%= ready %></div>\
        <div>disc: <%=disc %></div>\
        <div>color: <%=color %></div>"
    ),

    initialize: function () {
        _.bindAll(this, 'render', 'toggleReady');
        var events = {
        'click': 'toggleReady'
        };
        this.delegateEvents(events);
    },

    render: function () {
        var tmpl = this.template(this.model.toJSON());
        return this.$el.html(tmpl);
    },

    toggleReady: function () {
        var status = this.model.toJSON();
        status['ready'] = !status['ready'];
        RTReversi.EventDispatcher.trigger('changeStatus', status);
    }
});
