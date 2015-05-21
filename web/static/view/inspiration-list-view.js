define(['jquery', 'underscore', 'backbone', 'model/inspiration', 'view/modify-view'], 
function($, _, Backbone, Inspiration, ModifyView){
    
    var modifyView = new ModifyView({el: '#modify-area'});

    var InspirationListItemView = Backbone.View.extend({
        events: {
            'click  .sentence-wrapper': "modify",
        },
        next: null,

        model: new Inspiration.Model(),

        initialize: function() {
            this.listenTo(this.model, "change", this.render);
        },

        modify: function(e){
            e.preventDefault();
            modifyView.model = this.model;
            modifyView.render();
        },



        template: _.template($("#inpiration-list-item-template").html()),

        setModel: function(model){
            this.model = new Inspiration.Model(model);
            this.stopListening();
            this.listenTo(this.model, "change", this.modifyRender);
        },

        modifyRender: function(){
            this.undelegateEvents();
            var htmlContent = this.template({inspiration: this.model.attributes});
            this.$el.html($(htmlContent).html());
            this.delegateEvents();
        },

        render: function(){
            this.undelegateEvents();
            this.setElement(this.template({inspiration: this.model.attributes}));
        },

    });


    var InspirationListView = Backbone.View.extend({
        collection: new Inspiration.Collection(),

        setCollection: function(collection){ // 
            this.collection.reset(collection)
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