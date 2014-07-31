define(['d3', 'highlight', 'wq/pandas', 'wq/chart', 'wq/pages'],
function(d3, highlight, pandas, chart, pages) {

function setup() {
    pages.addRoute('datarequests/<slug>', 's', _onShow);
    pages.addRoute('', 's', showLatest);
}

function _onShow(match, ui, params, hash, evt, $page) {
    if (match[1] == "new") return;
    var elems = $page.find('svg');
    highlight.highlightBlock($page.find('code')[0]);
    if (!elems.length)
        return;
    showData(match[1], elems[0]);
}

function showData(id, elem) {
    // Multiple #clip defs break IE
    d3.selectAll('defs').remove();
    var svg = d3.select(elem);
    var text = svg.append('text')
        .attr('transform', 'translate(250, 140)')
        .attr('fill', '#666');
    var ndots = 0;
    var interval = setInterval(function() {
        var dots = "";
        for (var i = 0; i < ndots; i++)
            dots += ".";
        ndots += 1;
        if (ndots > 3)
            ndots = 0;
        text.text("Loading Chart" + dots);
    }, 500);
    pandas.get('/data/' + id + '/export.csv', function(data) {
        text.remove();
        clearInterval(interval);
        var plot = chart.timeSeries()
            .width(600)
            .height(300)
            .xticks(5)
            .id(function(dataset) {
                return dataset.parameter + '-' + dataset['site id'];
            })
            .label(function(dataset) {
                return (
                    dataset.parameter +
                    ' at ' +
                    dataset['site id'] +
                    ' (' +
                    dataset['site name'] +
                    ')'
                );
            });
        svg.datum(data).call(plot);
    });
}

function showLatest(match, ui, params, hash, evt, $page) {
    var svg;
    if ($page)
        svg = $page.find('svg')[0];
    else
        svg = d3.select('div.ui-page#index svg').node();
    showData('latest', svg);
}

return {
    'setup': setup,
    'showData': showData,
    'showLatest': showLatest
};

});
