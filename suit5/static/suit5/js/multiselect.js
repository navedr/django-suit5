/* global Suit, gettext */
// Keep Django's initialization API for filtered horizontal/vertical fields,
// including dynamically added inlines, while retaining the original select.
(function () {
    'use strict';

    window.SelectFilter = {
        init: function (fieldId) {
            var field = document.getElementById(fieldId);
            if (!field || fieldId.indexOf('__prefix__') !== -1) {
                return;
            }
            var $ = window.Suit && Suit.$;
            if (!$ || !$.fn.select2 || $(field).hasClass('select2-hidden-accessible')) {
                return;
            }

            $(field).select2({
                width: '100%',
                dropdownCssClass: 'suit-multiselect-dropdown',
                closeOnSelect: false
            });
            $(field).next('.select2-container').addClass('select2-container--suit-multiselect');
            $(field).next('.select2-container').find('.select2-search__field').attr(
                'aria-label', gettext('Search') + ' ' + (field.dataset.fieldName || field.name)
            );

            // Remove only Django's native multi-select keyboard hint, preserving
            // any application-specific help text (and its markup).
            var hint = gettext('Hold down "Control", or "Command" on a Mac, to select more than one.');
            var container = field.closest('.control-group, .form-row, td') || field.parentNode;
            container.querySelectorAll('.help, .helptext, .help-block, .help-inline').forEach(function (help) {
                var walker = document.createTreeWalker(help, NodeFilter.SHOW_TEXT);
                var node;
                while ((node = walker.nextNode())) {
                    node.textContent = node.textContent.replace(hint, '');
                }
                if (!help.textContent.trim()) {
                    help.hidden = true;
                }
            });
        }
    };

    function initialize(root) {
        root.querySelectorAll('select.selectfilter, select.selectfilterstacked').forEach(function (field) {
            window.SelectFilter.init(field.id);
        });
    }

    window.addEventListener('load', function () {
        initialize(document);
    });
    // Django 4.1+ emits native events; older versions call SelectFilter.init
    // directly from their inline formset code.
    document.addEventListener('formset:added', function (event) {
        initialize(event.target);
    });
})();
