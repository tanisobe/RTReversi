RTReversi.Views.Reversi = Backbone.View.extend({
    events: {
            'click': 'putDisc',
            'dblclick': 'removeDisc'
    },

    initialize: function () {
        _.bindAll(this, 'render', 'renderBoard', 'renderDisc', 'renderDiscs', 'initialize');
        RTReversi.EventDispatcher.on('renderReversi', this.render);
        var that = this;
        this.$el[0].addEventListener('mousemove',function(evt) {
            var rect = this.getBoundingClientRect();
            that.model.set('mouse', {
                x: evt.clientX - rect.left,
                y: evt.clientY - rect.top
            });
        });
        this.ctx = this.$el[0].getContext('2d');
    },

    renderBoard: function () {
        this.ctx.clearRect(0, 0, this.$el[0].width, this.$el[0].height);
        this.ctx.beginPath();
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

    renderDisc: function (x, y, color) {
        if ( color ){
            this.ctx.fillStyle = color;
            this.ctx.beginPath();
            this.ctx.arc(
                this.model.get('x') + this.model.get('tileLength') * (x + 0.5),
                this.model.get('y') + this.model.get('tileLength') * (y + 0.5),
                (this.model.get('tileLength')-10) / 2,
                0, 2 * Math.PI, false
            );
            this.ctx.fill();
            this.ctx.stroke();
            this.ctx.closePath();
        }
    },

    renderDiscs: function (param) {
        console.log('rederDiscs');
        console.log(param)
        for ( var x = 0; x < this.model.get('size'); x++){
            for ( var y = 0; y < this.model.get('size'); y++){
                this.renderDisc(x, y, param[x][y]);
            }
        }
    },

    render: function (param) {
        console.log(param);
        this.renderBoard();
        this.renderDiscs(param.surface);
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
