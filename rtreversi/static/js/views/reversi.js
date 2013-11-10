RTReversi.Views.Reversi = Backbone.View.extend({
    events: {
            'click': 'putDisc',
            'dblclick': 'removeDisc'
    },

    initialize: function () {
        _.bindAll(this, 'render', 'renderBoard', 'renderDisc', 'renderDiscs', 'renderBoardStatus', 'initialize');
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
        var ctx = this.$el[0].getContext('2d');
        ctx.clearRect(0, 0, this.$el[0].width, this.$el[0].height);
        ctx.beginPath();
        for ( var i = 0; i < this.model.get('size') ; i++) {
            for ( var j = 0; j < this.model.get('size') ; j++) {
                ctx.rect(
                    this.model.get('x') + i * this.model.get('tileLength'),
                    this.model.get('y') + j * this.model.get('tileLength'),
                    this.model.get('tileLength'),
                    this.model.get('tileLength')
                );
                ctx.lineWidth = 3;
                ctx.stroke();
            }
        }
        ctx.closePath();
    },

    renderObstacle: function (x, y) {
        console.log(x, y);
        var ctx = this.$el[0].getContext('2d');
        ctx.beginPath();
        ctx.fillStyle = 'Black';
        ctx.fillRect(
            this.model.get('x') + x * this.model.get('tileLength'),
            this.model.get('y') + y * this.model.get('tileLength'),
            this.model.get('tileLength'),
            this.model.get('tileLength')
        );
        ctx.stroke();
        ctx.closePath();
    },

    renderDisc: function (x, y, color) {
        if ( color ){
            if (color == 'Obstacle'){
                this.renderObstacle(x, y);
            }else{
                var ctx = this.$el[0].getContext('2d');
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(
                    this.model.get('x') + this.model.get('tileLength') * (x + 0.5),
                    this.model.get('y') + this.model.get('tileLength') * (y + 0.5),
                    (this.model.get('tileLength')-10) / 2,
                    0, 2 * Math.PI, false
                );
                ctx.fill();
                ctx.stroke();
                ctx.closePath();
            }
        }
    },

    renderDiscs: function (param) {
        for ( var x = 0; x < this.model.get('size'); x++){
            for ( var y = 0; y < this.model.get('size'); y++){
                this.renderDisc(x, y, param[x][y]);
            }
        }
    },

    renderBoardStatus: function (param) {
        var i = 1;
        var size = ( parseInt(this.$el[0].width) - 20 ) / ( Object.keys(param).length + 1 );
        var ctx = this.$el[0].getContext('2d');
        $.each( param, function( color, count ) {
            if ( color != 'null') {
                ctx.font = '30px Arial';
                ctx.fillStyle = 'black';
                ctx.fillText( color + ' : ' + count, size * i, 50);
                i++;
            }
        });
    },

    render: function (param) {
        this.renderBoard();
        this.renderDiscs(param.surface);
        this.renderBoardStatus(param.disc);
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
