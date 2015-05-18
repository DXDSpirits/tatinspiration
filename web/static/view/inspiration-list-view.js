define(['jquery', 'underscore', 'backbone', 'model/inspiration'], 
function($, _, Backbone, Inspiration){
    var InspirationListView = Backbone.View.extend({
        template: _.template($("#inpiration-list-item-template").html()),
        collection: new Inspiration.Collection(),

        setCollection: function(collection){ // 
            this.collection = new Inspiration.Collection(collection);
        },

        render: function(){
            var self = this;
            _.each(self.collection.models,function(obj){
                var htmlContent = self.template({inspiration: obj.attributes});
                // console.log(htmlContent);
                self.$el.append(htmlContent);
            })
        },
        hide: function(){
            this.$el.addClass("view-hide");
        },
        show: function(){
            this.$el.removeClass("view-hide");
        },
        clear:function(){
            this.collection.reset([]);
            this.$el.empty();
        }

    });


    return InspirationListView;

});