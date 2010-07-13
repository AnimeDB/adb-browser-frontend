document.createElement('header');
document.createElement('section');
document.createElement('nav');
document.createElement('footer');
document.createElement('time');

// Add no-wrap to table cells
jQuery(function () {
    $('td:not(:empty), th:not(:empty)').each(function () {
        if ($(this).css('white-space') === 'nowrap') {
            $(this).wrapInner(function () {
                return $('<div />').css('white-space', 'nowrap');
            });
        }
    })
})