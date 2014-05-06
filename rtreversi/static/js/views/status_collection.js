RTReversi.Views.StatusCollection = Backbone.View.extend({
    tagName: 'ul',

    initialize: function () {
        _.bindAll(this, 'update', 'render');
        RTReversi.EventDispatcher.on('updatePlayerStatus', this.update);
        this.listenTo(this.collection, 'add', this.render);
        this.listenTo(this.collection, 'change', this.render);
        this.listenTo(this.collection, 'delete', this.render);
    },

    update: function (param) {
        var that = this;
        var statusList = [];
        $.each( param, function (index, status) {
            statusList.push(new RTReversi.Models.Status(status));
        });
        this.collection.set(statusList);
    },

    render: function () {
        var that = this;
        this.$el.empty();
        this.collection.each(function(status) {
            var statusView = new RTReversi.Views.Status({model: status});
            that.$el.append(statusView.render());
        });
    }
});
