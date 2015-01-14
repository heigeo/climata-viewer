define(['d3', 'highlight', 'wq/pandas', 'wq/chart', 'wq/pages', 'wq/map', './layers'],
function(d3, highlight, pandas, chart, pages, map, layers) {

function setup() {
    pages.addRoute('<slug>/<slug>', 's', _onShow);
    pages.addRoute('', 's', _showLatest);
}

function _onShow(match, ui, params, hash, evt, $page) {
    var baseurl = match[1];
    if (match[2] == "new")
        return;
    if (baseurl != "projects" && baseurl != "datarequests")
        return;
    _showGraph(baseurl, match[2], $page);
}

function _showGraph(baseurl, itemid, $page) {
    var ids, labels, $elems;
    if (baseurl == "datarequests") {
        highlight.highlightBlock($page.find('code')[0]);
        ids = [itemid];
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
    var svg = d3.select(elem);
    var text = svg.append('text')
        .attr('transform', 'translate(50, 50)')
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

    var width = elem.parentElement.offsetWidth;
    var height = width * 0.5;
    if (height > 400)
        height = 400;
    var plot = chart.timeSeries()
        .width(width)
        .height(height)
        .outerFill('transparent')
        .innerFill('#f6f6f6')
        .xnice(d3.time.month)
        .xticks(Math.round(width / 150))
        .id(function(dataset) {
            return (
                dataset.group_id + '-' +
                dataset.parameter + '-' +
                dataset['site id'] + '-' +
                dataset.type
            );
        })
        .label(function(dataset) {
            if (dataset.type != '-') {
                return dataset['site id'] + " " + dataset.type;
            }
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

function _showLatest(match, ui, params, hash, evt, $page) {
    var projectid = $page.find('#latest-map').data('project-id');
    if (!projectid)
        return;
    _showGraph('projects', null, $page);
    map.config.maps.project.div = 'latest-map';
    map.createMap('project', projectid);
    map.config.maps.project.div = null;
    var m = map.maps['project-' + projectid];
    m.removeControl(m.attributionControl);
    m.removeControl(m.zoomControl);
}

return {
    'setup': setup,
    'showData': showData
};

});
