define(function(require) {
    var $ = require('jquery');
    var Jupyter = require('base/js/namespace');
    var utils = require('base/js/utils');

    var ajax = utils.ajax || $.ajax;

    var base_url = utils.get_body_data('baseUrl');

    function open_refine(w) {
        /* the url we POST to to start refine */
        var rsp_url = base_url + 'refineproxy';

        /* prepare ajax */
        var settings = {
            type: "POST",
            data: {},
            dataType: "json",
            success: function(data) {
                if (!("url" in data)) {
                    /* FIXME: visit some template */
                    return;
                }
                w.location = data['url'];
            },
            error : utils.log_ajax_error,
        }

        ajax(rsp_url, settings);
    }

    function load() {
        console.log("nbrefineproxy loading");
        if (!Jupyter.notebook_list) return;

        /* locate the right-side dropdown menu of apps and notebooks */
        var menu = $('.tree-buttons').find('.dropdown-menu');

        /* create a divider */
        var divider = $('<li>')
            .attr('role', 'presentation')
            .addClass('divider');

        /* add the divider */
        menu.append(divider);

        /* create our list item */
        var refine_item = $('<li>')
            .attr('role', 'presentation')
            .addClass('new-refineproxy');

        /* create our list item's link */
        var refine_link = $('<a>')
            .attr('role', 'menuitem')
            .attr('tabindex', '-1')
            .attr('href', '#')
            .text('OpenRefine')
            .on('click', function() {
                var w = window.open(undefined, Jupyter._target);
                open_refine(w);
            });

        /* add the link to the item and
         * the item to the menu */
        refine_item.append(refine_link);
        menu.append(refine_item);
    }

    return {
        load_ipython_extension: load
    };
});
