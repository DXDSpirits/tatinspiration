define(['jquery', 'underscore', 'backbone'], 
function($, _, Backbone){
    var InspirationListView = Backbone.View.extend({
        template: _.template($("#inpiration-list-item-template").html()),
        render: function(){
            var self = this;
            _.each(self.collection.models,function(obj){
                var htmlContent = self.template({inspiration: obj});
                // console.log(htmlContent);
                self.$el.append(htmlContent);
            })
        },

    });


    return InspirationListView;

});