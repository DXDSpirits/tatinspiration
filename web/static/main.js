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
            InspirationListView,
            $, _, Backbone) {

    // console.log($);
    // console.log(_);
    // console.log(Backbone);

    var Page = {};
    Page.currentPage = null;
    Page.main = new InspirationListView({el: "#main-view.sentence-container"});
    Page.labelFilter = new InspirationListView({el: "#label-filter-view.sentence-container"});
    Page.search = new InspirationListView({el: "#search-view.sentence-container"});

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
            $.get("/api/inspiration/?ordering=-id")
             .done(function(data){
                var inspirationData = data.objects;
                Page.main.clear();
                Page.main.next = data.meta.next;
                Page.main.setCollection(inspirationData);
                Page.main.render();
                Page.switchPage(Page.main);
             })


            var throttle = _.throttle(function() {
                if ($(window).scrollTop() + $(window).height() >= $('body').height() - 260) {
                    Backbone.trigger('next-page');
                }
            }, 200);
            $(window).off("scroll")
            $(window).scroll(throttle);
        },


        labelFilter: function(labelId){
            $(window).off("scroll")

            function _renderLabelFilter(data){
                var inspirationData = _.pluck(data.objects, "inspiration");
                Page.labelFilter.clear();
                Page.labelFilter.setCollection(inspirationData);
                Page.labelFilter.render();
                Page.switchPage(Page.labelFilter);
            }

            if(labelId === "0"){
                $.get("/api/nolabel-inspiration/")
                 .done(function(data){
                    var inspirationData = data.objects;
                    Page.labelFilter.clear();
                    Page.labelFilter.setCollection(inspirationData);
                    Page.labelFilter.render();
                    Page.switchPage(Page.labelFilter);
                 })

                 return ;
            }


            $.get("/api/labelinspirationrelationship/?label="+labelId)
             .done(function(data){
                _renderLabelFilter(data);
             });
        },

        search: function(keyword){
            $(window).off("scroll")
            $.get("/api/inspiration/search?q="+keyword)
             .done(function(data){
                var inspirationData = data.objects;
                Page.search.clear();
                Page.search.setCollection(inspirationData);
                Page.search.render();
                Page.switchPage(Page.search);

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

    Backbone.on("next-page", function(){
        var curTime = new Date();
        var $loading = $(".loading-container").show();

        if(! Page.main.next){
            $loading.hide()
            return ;
        }

        function _render(data){
            Page.main.next = data.meta.next;
            Page.main.setCollection(data.objects);
            Page.main.render();
            Page.switchPage(Page.main);
        }

        $.get(Page.main.next)
         .done(function(data){
            var delta = (new Date()) - curTime;
            if( delta < 550){
                _.delay(function(){
                    _render(data);
                }, 550 - delta);
            }else{
                _render(data);
            }
            
         })

    })


    Backbone.history.start()





});






