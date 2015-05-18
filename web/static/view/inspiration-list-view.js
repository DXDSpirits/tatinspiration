define(['jquery', 'underscore', 'backbone', 'model/inspiration'], 
function($, _, Backbone, Inspiration){

    var InspirationListItemView = Backbone.View.extend({
        template: _.template($("#inpiration-list-item-template").html()),

        setModel: function(model){
            this.model = new Inspiration.Model(model);
        },

        render: function(){
            this.undelegateEvents();
            this.setElement(this.template({inspiration: this.model.attributes}));
        },

    });


    var InspirationListView = Backbone.View.extend({
        collection: new Inspiration.Collection(),

        setCollection: function(collection){ // 
            this.collection = new Inspiration.Collection(collection);
        },

        render: function(){
            var self = this;
            _.each(self.collection.models,function(obj){
                var iliv = new InspirationListItemView();
                iliv.setModel(obj.attributes);
                iliv.render();
                self.$el.append(iliv.$el);

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