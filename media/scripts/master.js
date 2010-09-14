"use strict";

jQuery.fn.hideitems = function(visible) {
    if (visible == undefined) {
        visible = 5
    }
    return this.each(function () {
        var element = $(this),
            count = $('li', element).size(),
            link = $('> a', element),
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
                    element.hideitems(visible);
                });
            }
            
            link.text('mostra tutti');
        }
    });
};

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

$(function () {
    /**
     * Display only the first 'n' items in the cast and genres lists.
     */
    $('body#movie-details .cast').hideitems();
    $('body#movie-details .genres').hideitems(8);
    
    /**
     * Add the focus class to surrounding paragraphs of inputs and make they
     * act as labels.
     */
    $('p > input').focus(function () {
        $(this).parent().addClass('focus');
    }).blur(function () {
        $(this).parent().removeClass('focus');
    }).parent().click(function () {
        $('input', this).focus();
    });
    
    /**
     * Focus the list name textbox on page loading.
     */
    $('body#lists_create section form input').focus();
    $('body#checker_index section form input').focus();
    $('body#login #id_username').focus().select();
    $('#messages li').each(function () {
        $(this).append($('<a>×</a>').click(function () {
            var li = $(this).parent(),
                ul = li.parent();
        
            if ($('li', ul).size() == 1) {
                ul.slideUp(300, function () {
                    ul.remove();
                });
            } else {
                li.slideUp(200, function () {
                    li.remove();
                    if (!$('li', ul).size()) {
                        ul.stop().slideUp(200, function () {
                            ul.remove();
                        });
                    }
                });
            }
        }))
    });
    
    /**
     * Automatically wraps the content of buttons and buttonlinks in a span to
     * provide greater styling.
     */
    $('button, a.button').wrapInner('<span/>');
    
    $('section table').wrap('<div class="table"/>');
});

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
