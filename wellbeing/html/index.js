// Generated by CoffeeScript 1.9.2
(function() {
  var Hexagon, changeView, dimensions, height, hexH, hexS, hexW, margin, radius, width;

  hexS = 35;

  hexH = Math.sqrt(3) * hexS;

  hexW = Math.sqrt(3) / 2 * hexH;

  radius = hexS;

  height = Math.floor($(window).height() / hexH) * hexH;

  width = Math.floor($(window).width() / hexW) * hexW;

  margin = {
    x: hexW,
    y: hexH
  };

  dimensions = ['education', 'jobs', 'income', 'safety', 'health', 'environment', 'civic engagement', 'accessiblity to services', 'housing', 'community', 'life satisfaction'];

  Hexagon = (function() {
    var d3_hexbinAngles;

    function Hexagon(radius1, mdsX, mdsY, details) {
      var _x, _y, _z, q, r, rx, ry, rz, x_diff, y_diff, z_diff;
      this.radius = radius1;
      this.details = details;
      q = (mdsX * Math.sqrt(3) / 3.0 - mdsY / 3.0) / this.radius;
      r = mdsY * 2 / 3.0 / this.radius;
      _x = q;
      _z = r;
      _y = -_x - _z;
      rx = Math.round(_x);
      ry = Math.round(_y);
      rz = Math.round(_z);
      x_diff = Math.abs(Math.abs(rx) - Math.abs(_x));
      y_diff = Math.abs(Math.abs(ry) - Math.abs(_y));
      z_diff = Math.abs(Math.abs(rz) - Math.abs(_z));
      if ((x_diff > y_diff && y_diff > z_diff)) {
        rx = -ry - rz;
      } else if (y_diff > z_diff) {
        ry = -rx - rz;
      } else {
        rz = -rx - ry;
      }
      this.q = rx;
      this.r = rz;
      this.getCenterCoordinates();
    }

    d3_hexbinAngles = d3.range(0, 2 * Math.PI, Math.PI / 3);

    Hexagon.prototype.getCornerCoordinates = function() {
      var x0, y0;
      x0 = 0;
      y0 = 0;
      return d3_hexbinAngles.map((function(_this) {
        return function(angle) {
          var dx, dy, x1, y1;
          x1 = Math.sin(angle) * _this.radius;
          y1 = -Math.cos(angle) * _this.radius;
          dx = x1 - x0;
          dy = y1 - y0;
          x0 = x1;
          y0 = y1;
          return [dx, dy];
        };
      })(this));
    };

    Hexagon.prototype.getSVGString = function() {
      var points, s;
      points = this.getCornerCoordinates();
      return s = ("M " + this.x + " " + this.y + " m ") + points.join(" l ");
    };

    Hexagon.prototype.getCenterCoordinates = function() {
      this.x = this.radius / 2.0 * Math.sqrt(3) * (this.q + this.r / 2.0) + width / 4;
      return this.y = this.radius / 2.0 * 1.5 * this.r + height / 4;
    };

    return Hexagon;

  })();

  changeView = function(focusId, k) {
    return $.getJSON("http://127.0.0.1:5000/" + focusId + "/" + k, function(response) {
      var data, fo, g, scaleH, scaleW, svg, tooltip, xMax, xMin, xValues, yMax, yMin, yValues;
      xValues = [];
      yValues = [];
      response.coordinates.forEach(function(coordinate) {
        xValues.push(coordinate[0]);
        return yValues.push(coordinate[1]);
      });
      xMax = Math.max.apply(Math, xValues);
      xMin = Math.min.apply(Math, xValues);
      yMax = Math.max.apply(Math, yValues);
      yMin = Math.min.apply(Math, yValues);
      scaleH = d3.scale.linear().range([-height / 2 + hexH, height / 2 - hexH]).domain([yMin, yMax]);
      scaleW = d3.scale.linear().range([-width / 2 + hexW, width / 2 - hexW]).domain([xMin, xMax]);
      data = [];
      response.coordinates.forEach(function(coordinate, i) {
        var h, x, y;
        x = coordinate[0], y = coordinate[1];
        h = new Hexagon(radius, scaleW(x), scaleH(y), response.details[i]);
        return data.push(h);
      });
      data = data.reverse();
      svg = d3.select("#canvas").html("").append("svg").attr("width", width).attr("height", height);
      tooltip = d3.select("#canvas").append("div").attr("class", "tooltip row").style("opacity", 0);
      g = svg.selectAll(".hexagon").data(data).enter().append("g").attr("class", "hexagon").attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      }).on("click", function(d) {
        console.log(d);
        return changeView(d.details.id, k);
      }).on("mouseover", function(d) {
        var fixedX, htmlText, realW;
        tooltip.transition().delay(100).duration(100).style('opacity', .9);
        htmlText = "<table>" + dimensions.map(function(dimension) {
          return "<tr><td class='text-capitalize'>" + dimension + "</td><td><svg width='100' height='10'><rect width='" + (parseFloat(d.details[dimension]) * 10) + "' height='10' fill='#c5e7ed'></rect></svg></td><td>" + d.details[dimension] + "</td></tr>";
        }).join('') + "</table>";
        tooltip.html(htmlText);
        realW = tooltip.node().getBoundingClientRect().width;
        fixedX = d3.event.pageX + 30;
        if (fixedX > $(window).width() / 2) {
          fixedX = d3.event.pageX - realW;
        }
        return tooltip.style("left", fixedX + "px").style("top", d3.event.pageY + "px");
      }).on("mouseout", function() {
        tooltip.html('');
        return tooltip.transition().delay(100).duration(100).style('opacity', 0);
      });
      g.append("path").attr("d", function(h) {
        return h.getSVGString();
      }).attr("fill", function(d) {
        if (d.details.id === focusId) {
          return "#c5e7ed";
        } else {
          return "#ededed";
        }
      }).attr("id", function(d) {
        return d.r + " " + d.q;
      });
      fo = g.append('foreignObject').attr({
        'width': hexW,
        'height': hexH,
        'class': 'hexagon-label'
      }).attr('x', function(d) {
        return d.x - hexW / 2;
      }).attr('y', function(d) {
        return d.y - hexH / 2;
      });
      return fo.append('xhtml:div').style('height', hexH + "px").append('div').html((function(_this) {
        return function(d) {
          return d.details.country + "<br>" + d.details.region;
        };
      })(this));
    });
  };

  $(function() {
    var focusId, k;
    k = 10;
    focusId = Math.floor(Math.random() * 397);
    return changeView(focusId, k);
  });

}).call(this);
