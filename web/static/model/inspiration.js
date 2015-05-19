define(['jquery', 'underscore', 'backbone'], 
function($, _, Backbone){
    var Inspiration = Backbone.Model.extend({

        post: function(){
            jQuery.ajaxSettings.traditional = true;
            var url = "/api/inspiration/"+ this.get("id") +"/modify";
            $.post(url, {
                content: this.get("content"),
                labels: _.pluck(this.get("labels"), "name"),
            })
        },

    });

    var InspirationCollection = Backbone.Collection.extend({
        model: Inspiration,
    });


    return {
        Model: Inspiration,
        Collection: InspirationCollection
    };

});