define(['d3', 'wq/pandas', 'wq/chart', 'wq/pages'],
function(d3, pandas, chart, pages) {

function setup() {
    pages.addRoute('datarequests/<slug>', 's', _onShow);
}

function _onShow(match, ui, params, hash, evt, $page) {
    var elems = $page.find('svg');
    if (!elems.length)
        return;
    showData(match[1], elems[0]);
}

function showData(id, elem) {
    var svg = d3.select(elem);
    pandas.get('/data/' + id + '/export.csv', function(data) {
        var plot = chart.timeSeries()
            .width(600)
            .height(300)
            .id(function(dataset) {
                return dataset.parameter + '-' + dataset['site id'];
            })
            .label(function(dataset) {
                return (
                    dataset.parameter
                    + ' at '
                    + dataset['site id']
                    + ' ('
                    + dataset['site name']
                    + ')'
                );
            });
        svg.datum(data).call(plot);
    });
}

return {
    'setup': setup,
    'showData': showData
};

});
