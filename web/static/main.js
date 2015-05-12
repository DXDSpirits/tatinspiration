require.config({
    baseUrl: '/static/',
    shim : {
        "bootstrap" : { "deps" :['jquery'] },
        // "jquery-cookie"  : ["jquery"]
    },
    paths: {
        select2: 'libs/select2/js/select2.full',
        jquery: 'libs/jquery',
        underscore: 'libs/underscore', 
        backbone: 'libs/backbone',
        domReady: 'libs/domReady',
        bootstrap: 'libs/bootstrap/js/bootstrap'
    }
});

require(['jquery', 'underscore', 'backbone', 'domReady!', 'bootstrap', 'select2'], 
        function($, _, Backbone) {

    // console.log($);
    // console.log(_);
    // console.log(Backbone);
    $("#label-input").select2({
        placeholder: "labels",
        tags: true,
        tokenSeparators: [',', ' ']
    });

    var inpirationListItemTemplate = _.template($("#inpiration-list-item-template").html())

    var router = new (Backbone.Router.extend({
        routes: {
            "labelFilter=:labelId": "labelFilter", // #search/kiwis/p7
            "search=:keyword": "search"
        },

        labelFilter: function(labelId){
            $.get("/api/labelinspirationrelationship/?label="+labelId)
             .done(function(data){
                console.log(data)
                var $sentenceContainer = $('.sentence-container');
                $sentenceContainer.html("");
                _.each(data.objects,function(obj){
                    var htmlContent = inpirationListItemTemplate(obj);
                    console.log(htmlContent);
                    $sentenceContainer.append(htmlContent)
                })

             });
        },

        search: function(keyword){
            $.get("/api/inspiration/search?q="+keyword)
             .done(function(data){
                console.log(data)
                var $sentenceContainer = $('.sentence-container');
                $sentenceContainer.html("");
                _.each(data.objects,function(obj){
                    var htmlContent = inpirationListItemTemplate({inspiration: obj});
                    console.log(htmlContent);
                    $sentenceContainer.append(htmlContent)
                })

             });
        },

    }))


    $(document).on("click", "#search-btn", function(e){
        var keyword = $("#keyword-input").val();
        router.navigate("search="+keyword, {trigger: true});
    })

    $(document).on("submit", "#search-form", function(e){
        e.preventDefault();
        var keyword = $("#keyword-input").val();
        router.navigate("search="+keyword, {trigger: true});
    })

    Backbone.history.start()





});






