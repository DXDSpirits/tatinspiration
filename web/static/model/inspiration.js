define(['jquery', 'underscore', 'backbone'], 
function($, _, Backbone){
    var Inspiration = Backbone.Model.extend({

    });

    var InspirationCollection = Backbone.Collection.extend({
        model: Inspiration,
    });


    return {
        model: Inspiration,
        collection: InspirationCollection
    };

});