var width = $('#chart-width').width(),
  barHeight = 20;

var x = d3.scale.linear()
    .domain([0, 45])
    .range([0, width]);

var doBarNegChart = function(){
  var data = [{n:45, name:"Demmin"},{n:44, name:"Ahrenshoop"},{n:44, name:"Wustrow"},{n:44, name:"Dierhagen"}, {n:41, name:"Warrenzin"},{n:41, name:"Dargun"}, {n:41, name:"Nossendorf"}, {n:40, name:"Anklam"}, {n:40, name:"Neustrelitz"}, {n:39, name:"Schönfeld"}, {n:39, name:"Userin"},{n:39, name:"Verchen"},{n:38, name:"Ribnitz"},{n:37, name:"Wokuhl"},{n:37, name:"Butzow"},{n:37, name:"Blesewitz"}]

  var chart = d3.select(".chart-neg")
      .attr("width", width)
      .attr("height", barHeight * data.length);

  var bar = chart.selectAll("g")
      .data(data)
    .enter().append("g")
      .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

  bar.append("rect")
      .attr("width", function(d) {return x(d.n);})
      .attr("height", barHeight - 1)
      .style("fill", "#a50026");

  bar.append("text")
      .attr("x", function(d) { return x(d.n) - 3; })
      .attr("y", barHeight / 2)
      .attr("dy", ".35em")
      .text(function(d) { return "+" + d.n + " min"; });

  bar.append("text")
      .attr("x", 3)
      .attr("y", barHeight / 2)
      .attr("dy", ".35em")
      .style("text-anchor","start")
      .text(function(d) { return d.name; });
};

var doBarPosChart = function(){
  var data = [{n:30, name:"Wittenförden"},{n:29, name:"Klein Rogahn"},{n:28, name:"Kuhblank"}]

  var chart = d3.select(".chart-pos")
      .attr("width", width)
      .attr("height", barHeight * data.length);

  var bar = chart.selectAll("g")
      .data(data)
    .enter().append("g")
      .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

  bar.append("rect")
      .attr("width", function(d) {return x(d.n);})
      .attr("height", barHeight - 1)
      .style("fill", "#4575b4");

  bar.append("text")
      .attr("x", function(d) { return x(d.n) - 3; })
      .attr("y", barHeight / 2)
      .attr("dy", ".35em")
      .text(function(d) { return "-" + d.n + " min"; });

  bar.append("text")
      .attr("x", 3)
      .attr("y", barHeight / 2)
      .attr("dy", ".35em")
      .style("text-anchor","start")
      .text(function(d) { return d.name; });
};

doBarNegChart();
doBarPosChart();

window.onload = function() {
  cartodb.createVis('map1', 'https://filter.cartodb.com/api/v2/viz/4ad72676-4835-11e5-b84d-0e0c41326911/viz.json', {"zoom": 8, "center_lat": 53.897441, "center_lon": 12.606970})
      .done(function(vis, layers) {
           vis.map.set({
          minZoom: 6,
          maxZoom: 10
        });
      })
      .error(function(err) {
        console.log(err);
      });

  cartodb.createVis('map2', 'https://filter.cartodb.com/api/v2/viz/570f0a04-4843-11e5-b25e-0e018d66dc29/viz.json', {"zoom": 8, "center_lat": 53.897441, "center_lon": 12.606970})
      .done(function(vis, layers) {
           vis.map.set({
          minZoom: 6,
          maxZoom: 10
        });
      })
      .error(function(err) {
        console.log(err);
      });
  cartodb.createVis('map3', 'https://filter.cartodb.com/api/v2/viz/3fd97510-4846-11e5-b9e2-0e853d047bba/viz.json', {"zoom": 8, "center_lat": 53.897441, "center_lon": 12.606970})
      .done(function(vis, layers) {
           vis.map.set({
          minZoom: 6,
          maxZoom: 10
        });
      })
      .error(function(err) {
        console.log(err);
      });
};
