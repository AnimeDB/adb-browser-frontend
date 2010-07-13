"use strict";

function hideitems(selector, visible) {
    var element = $(selector),
        count = $('li', element).size(),
        link = $('> a', selector),
        msg  = $('<span>e altri ' + (count - visible) + '.</span>');
    
    if (count > visible) {
        $('li:eq(' + (visible - 1) + ')', element).addClass('last');
        $('li:gt(' + (visible - 1) + ')', element).addClass('hidden');
        element.append(msg);
        
        if (link.size() == 0) {
            link = $('<a href="#"></a>').appendTo(element).toggle(function () {
                $('li', element).removeClass('hidden').removeClass('last');
                $(this).text('mostra solo i primi ' + visible);
                $('> span', element).remove();
            }, function () {
                hideitems(selector, visible);
            });
        }
        
        link.text('mostra tutti');
    }
}

$(function () {
    $('body#details').each(function () {
        hideitems('.cast', 5);
        hideitems('.genres', 8);
    });
});