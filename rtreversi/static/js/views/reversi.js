RTReversi.Views.Reversi = Backbone.View.extend({
    events: {
            'click': 'putDisc',
            'dblclick': 'removeDisc'
    },

    initialize: function () {
        RTReversi.EventDispatcher.on('render-reversi', this.render);
        var that = this;
        this.$el[0].addEventListener('mousemove',function(evt) {
            var rect = this.getBoundingClientRect();
            that.model.set('mouse', {
                x: evt.clientX - rect.left,
                y: evt.clientY - rect.top
            });
        });
        this.ctx = this.$el[0].getContext('2d');
        this.render();
    },

    renderBoard: function () {
        for ( var i = 0; i < this.model.get('size') ; i++) {
            for ( var j = 0; j < this.model.get('size') ; j++) {
                this.ctx.rect(
                    this.model.get('x') + i * this.model.get('tileLength'),
                    this.model.get('y') + j * this.model.get('tileLength'),
                    this.model.get('tileLength'),
                    this.model.get('tileLength')
                );
                this.ctx.lineWidth = 3;
                this.ctx.stroke();
            }
        }
        this.ctx.closePath();
    },

    renderDisc: function () {
    },

    render: function () {
        this.renderBoard();
    },

    getBoardPos: function () {
        var mouse = this.model.get('mouse');
        if ( this.model.get('x') < mouse.x &&
            mouse.x < this.model.get('x') + this.model.get('tileLength') * this.model.get('size') &&
            this.model.get('y') < mouse.y
            && mouse.y < this.model.get('y') + this.model.get('tileLength') * this.model.get('size')) {
            return {
                x: Math.floor((mouse.x - this.model.get('x')) / this.model.get('tileLength')),
                y: Math.floor((mouse.y - this.model.get('y')) / this.model.get('tileLength'))
            };
        }
        return {
            x: null,
            y: null
        };
    },

    putDisc: function () {
        var pos = this.getBoardPos();
        RTReversi.EventDispatcher.trigger('putDisc', pos);
    },

    removeDisc: function () {
        var pos = this.getBoardPos();
        RTReversi.EventDispatcher.trigger('removeDisc', pos);
    }
});
