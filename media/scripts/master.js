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


function tableFromList(list) {
    var table = $('<table></table>'), row;
    
    $('li', list).each(function (n) {
        if (n % 7 == 0) {
            row = $('<tr></tr>').appendTo(table);
        }
        $('<td></td>').html($(this).html()).appendTo(row);
    });
    
    return table;
}


// Browse menu item support
$(function () {
    var container = $('<div></div>').appendTo('#browse-menu-item')
                                    .append($('#browse-menu-item > ul'));
    
    $('#browse-menu-item li ul').each(function (n) {
        var table = tableFromList(this).appendTo(container);
        $(this).remove();
    });
    
    $('> ul > li', container).click(function () {
        var self = $(this);
        if (!self.hasClass('selected')) {
            $('.selected', container).removeClass('selected');
            self.addClass('selected');
            $('table', container).eq(self.index()).addClass('selected');
        }
    }).eq(0).click();
});
