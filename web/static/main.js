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

require(['model/inspiration', 
         'view/inspiration-list-view',
         'jquery', 'underscore', 'backbone', 
         'bootstrap', 'select2', 'domReady!'], 
        function(
            Inspiration,
            InspirationView,
            $, _, Backbone) {

    // console.log($);
    // console.log(_);
    // console.log(Backbone);
    $("#label-input").select2({
        placeholder: "labels",
        tags: true,
        tokenSeparators: [',', ' ']
    });

    var Page = {};
    Page.currentPage = null;
    Page.labelFilter = new InspirationView({el: "#label-filter-view.sentence-container"});

    Page.switchPage = function(page){
        if(Page.currentPage === page){
            return ;
        }


        if(Page.currentPage){
            Page.currentPage.hide();
        }

        Page.currentPage = page;
        page.show();

    }


    var router = new (Backbone.Router.extend({
        routes: {
            "": "index",
            "labelFilter=:labelId": "labelFilter", // #search/kiwis/p7
            "search=:keyword": "search"
        },

        index: function(){
            // infinite scroll
            // var throttle = _.throttle(function() {
            //     if ($(window).scrollTop() + $(window).height() >= $('body').height() - 260) {
            //         Backbone.trigger('next-page');
            //     }
            // }, 200);
            // $(window).off("scroll")
            // $(window).scroll(throttle);
        },

        labelFilter: function(labelId){
            $.get("/api/labelinspirationrelationship/?label="+labelId)
             .done(function(data){
                var inspirationData = _.pluck(data.objects, "inspiration");
                Page.labelFilter.clear();
                Page.labelFilter.setCollection(inspirationData);
                Page.labelFilter.render();
                Page.switchPage(Page.labelFilter);
             });
        },

        search: function(keyword){
            $.get("/api/inspiration/search?q="+keyword)
             .done(function(data){
                // console.log(data)
                var $sentenceContainer = $('.sentence-container');
                $sentenceContainer.html("");
                _.each(data.objects,function(obj){
                    var htmlContent = inpirationListItemTemplate({inspiration: obj});
                    // console.log(htmlContent);
                    $sentenceContainer.append(htmlContent)
                })

             });
        },

    }))

    $(document).on("click", "#search-btn", function(e){
        var keyword = $("#keyword-input").val();
        router.navigate("search="+keyword, {trigger: true});
        $(window).off("scroll")
    })

    $(document).on("submit", "#search-form", function(e){
        e.preventDefault();
        var keyword = $("#keyword-input").val();
        router.navigate("search="+keyword, {trigger: true});
        $(window).off("scroll")
    })

    Backbone.on("next-page", function(){
        var curTime = new Date();
        var $loading = $(".loading-container").show();

        var inspirationId = $("[data-inspiration-id]").last().data("inspiration-id");
        if(inspirationId === 1){
            $loading.hide()
            return ;
        }

        function _render(data){
            $loading.hide()
            var $sentenceContainer = $('.sentence-container');
            // $sentenceContainer.html("");
            _.each(data.objects,function(obj){
                var htmlContent = inpirationListItemTemplate({inspiration: obj});
                // console.log(htmlContent);
                $sentenceContainer.append(htmlContent)
            })
        }


        $.get("/api/inspiration/?ordering=-id&id__lt=" + inspirationId)
         .done(function(data){
            var delta = (new Date()) - curTime;
            if( delta < 350){
                _.delay(function(){
                    _render(data);
                }, 800);
            }else{
                _render(data);
            }
            
         })

    })


    Backbone.history.start()





});






