define(['jquery', 'underscore', 'backbone'], 
function($, _, Backbone){
    var Inspiration = Backbone.Model.extend({

    });

    var InspirationCollection = Backbone.Collection.extend({
        model: Inspiration,
    });


    return {
        Model: Inspiration,
        Collection: InspirationCollection
    };

});