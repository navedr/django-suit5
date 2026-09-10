(function () {
    'use strict';
    var input = document.getElementById('dashboard-filter');
    if (!input) return;
    var cards = Array.from(document.querySelectorAll('#content-main .dashboard-app'));
    var status = document.getElementById('dashboard-filter-status');
    var previousOpen = null;
    input.addEventListener('input', function () {
        var query = input.value.trim().toLocaleLowerCase();
        if (query && !previousOpen) previousOpen = cards.map(function (card) { return card.open; });
        var matches = 0;
        cards.forEach(function (card, index) {
            var sectionMatches = card.querySelector('.dashboard-app-name').textContent.toLocaleLowerCase().includes(query);
            var visibleRows = 0;
            card.querySelectorAll('tr').forEach(function (row) {
                var label = row.querySelector('th');
                var match = !query || sectionMatches || (label && label.textContent.toLocaleLowerCase().includes(query));
                row.hidden = !match;
                if (match) visibleRows++;
            });
            card.hidden = !!query && !sectionMatches && !visibleRows;
            if (!card.hidden) matches++;
            if (query) card.open = !card.hidden;
            else if (previousOpen) card.open = previousOpen[index];
        });
        status.hidden = !query || matches > 0;
        if (!query) previousOpen = null;
    });
})();
