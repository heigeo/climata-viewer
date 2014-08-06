define(['d3', 'highlight', 'wq/pandas', 'wq/chart', 'wq/pages', './layers'],
function(d3, highlight, pandas, chart, pages, layers) {

function setup() {
    pages.addRoute('<slug>/<slug>', 's', _onShow);
    pages.addRoute('', 's', showLatest);
}

function _onShow(match, ui, params, hash, evt, $page) {
    var baseurl = match[1], $elems, ids, labels;

    if (match[2] == "new")
        return;
    if (baseurl != "projects" && baseurl != "datarequests")
        return;

    if (baseurl == "datarequests") {
        highlight.highlightBlock($page.find('code')[0]);
        ids = [match[2]];
    } else {
        ids = [];
        labels = {};
        layers.getLayers($page).forEach(function(d){
            ids.push(d.id);
            labels[d.id] = d.label;
        });
    }

    $elems = $page.find('svg');
    if (ids.length && $elems.length)
        showData(ids, $elems[0], labels);
}

function showData(ids, elem, labels) {
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

    var plot = chart.timeSeries()
        .width(600)
        .height(300)
        .xnice(d3.time.month)
        .xticks(5)
        .id(function(dataset) {
            return (
                dataset.group_id + '-' +
                dataset.parameter + '-' +
                dataset['site id']
            );
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

    if (labels) {
        plot.legendItems(function() {
            return ids;
        });
        plot.legendItemId(function(id) {
            return id;
        });
        plot.legendItemLabel(function(id) {
            return labels[id];
        });
        plot.cscale(_makeScale());
    }
    window.plott=plot;

    ids.forEach(function(id) {
        pandas.get('/data/' + id + '/export.csv', _plot(id));
    });

    var data = [];
    function _plot(id) {
        return function(newdata) {
            if (interval) {
                text.remove();
                clearInterval(interval);
            }
            newdata.forEach(function(d) {
                d.group_id = id;
            });
            data = data.concat(newdata);
            svg.datum(data).call(plot);
        };
    }

    function _makeScale() {
        var _scale = d3.scale.ordinal()
            .domain(ids)
            .range(layers.hexColors);

        function scale(val) {
            var group = val.split('-')[0];
            return _scale(group);
        }
        return scale;
    }
}

function showLatest(match, ui, params, hash, evt, $page) {
    var svg;
    if ($page)
        svg = $page.find('svg')[0];
    else
        svg = d3.select('div.ui-page#index svg').node();
    showData(['latest'], svg);
}

return {
    'setup': setup,
    'showData': showData,
    'showLatest': showLatest
};

});
