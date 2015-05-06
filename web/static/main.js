require.config({
    baseUrl: 'static/',
    paths: {
        jquery: 'libs/jquery',
        underscore: 'libs/underscore', 
        backbone: 'libs/backbone',
        domReady: 'libs/domReady',
        bootstrap: 'libs/bootstrap/js/bootstrap'
    }
});

require(['jquery', 'underscore', 'backbone', 'domReady!', 'bootstrap'], 
        function($, _, Backbone) {

    console.log($);
    console.log(_);
    console.log(Backbone);



});






