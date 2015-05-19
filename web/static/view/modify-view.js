define(['jquery', 'underscore', 'backbone'], 
function($, _, Backbone){

    var ModifyView = Backbone.View.extend({
        events : {
            'click .save-btn': 'save',
        },

        save: function(e){
            var self = this;
            e.preventDefault();
            var content = this.$("[name=content]").val();
            this.model.set("content", content);
            var labels = []
            _.each($("option:selected"), function(option){
                var $option = $(option);
                var label = {}
                label.id = $option.attr("value");
                label.name = $option.html();
                labels.push(label);
            })
            this.model.set("labels", labels);
            this._postSave();
            // this.remove();
        },

        _postSave: function(){ // save to server
            this.model.post();
        },


        template: _.template($("#modify-board-template").html()),


        render: function(){
            this.undelegateEvents();
            var self = this;
            var htmlContent = this.template({inspiration: this.model.attributes});
            this.$el.html(htmlContent);
            _.each(this.model.get("labels"), function(label){
                console.log(label);
                this.$("[value=" + label.id +"]").attr("selected", "selected");
            })


            this.$("#label-input").select2({
                placeholder: "labels",
                tags: true,
                tokenSeparators: [',', ' ']
            });
            this.delegateEvents();
        }


    });

    return ModifyView;



});