hexS = 35
hexH = Math.sqrt(3) * hexS
hexW = Math.sqrt(3)/2 * hexH

radius = hexS
height = Math.floor($(window).height() / hexH) * hexH
width = Math.floor($(window).width() / hexW) * hexW

margin =
  x: hexW
  y: hexH

dimensions = ['education','jobs','income','safety','health','environment','civic engagement','accessiblity to services','housing','community','life satisfaction']

class Hexagon
  constructor: (@radius, mdsX, mdsY, @details) ->
    q = (mdsX * Math.sqrt(3) / 3.0 - mdsY / 3.0) / (@radius)
    r = mdsY * 2 / 3.0 / ( @radius)

    _x = q
    _z = r
    _y = -_x - _z

    rx = Math.round(_x)
    ry = Math.round(_y)
    rz = Math.round(_z)

    x_diff = Math.abs(Math.abs(rx) - Math.abs(_x))
    y_diff = Math.abs(Math.abs(ry) - Math.abs(_y))
    z_diff = Math.abs(Math.abs(rz) - Math.abs(_z))

    if x_diff > y_diff > z_diff
        rx = -ry - rz
    else if y_diff > z_diff
        ry = -rx - rz
    else
        rz = -rx - ry

    @q = rx
    @r = rz

    this.getCenterCoordinates()

  d3_hexbinAngles = d3.range(0, 2 * Math.PI, Math.PI / 3)

  getCornerCoordinates: () ->
    x0 = 0
    y0 = 0

    d3_hexbinAngles.map (angle) =>
      x1 = Math.sin(angle) * this.radius
      y1 = -Math.cos(angle) * this.radius
      dx = x1 - x0
      dy = y1 - y0
      x0 = x1
      y0 = y1
      [dx, dy]

  getSVGString: () ->
    points = this.getCornerCoordinates()
    s = "M #{@x} #{@y} m " + points.join " l "


  getCenterCoordinates: ->
    @x = @radius / 2.0 * Math.sqrt(3) * (@q + @r/2.0) + width/4
    @y = @radius / 2.0 * 1.5 * (@r) + height/4

changeView = (focusId, k) ->
  $.getJSON "http://127.0.0.1:5000/#{focusId}/#{k}", (response) ->

    # this breaks the apsect ratio... but otherwise the there would be too much unused space
    xValues = []
    yValues = []
    response.coordinates.forEach (coordinate) ->
        xValues.push coordinate[0]
        yValues.push coordinate[1]

    xMax = Math.max xValues...
    xMin = Math.min xValues...
    yMax = Math.max yValues...
    yMin = Math.min yValues...

    scaleH = d3.scale.linear()
      .range [-height / 2 + hexH, height / 2 - hexH]
      .domain [yMin, yMax]

    scaleW = d3.scale.linear()
      .range [-width/ 2 + hexW, width / 2 - hexW]
      .domain [xMin, xMax]

    data = []
    response.coordinates.forEach (coordinate, i) ->
      [x, y] = coordinate
      h = new Hexagon radius, scaleW(x), scaleH(y), response.details[i]
      data.push h

    # focus will always be on the top
    data = data.reverse()

    svg = d3.select("#canvas").html("").append("svg")
      .attr "width", width
      .attr "height", height

    tooltip = d3.select("#canvas").append "div"
      .attr "class", "tooltip row"
      .style "opacity", 0

    g = svg.selectAll(".hexagon")
        .data(data)
      .enter().append("g")
        .attr "class", "hexagon"
        .attr "transform", (d) -> "translate(#{d.x},#{d.y})"
        .on "click", (d) -> 
          console.log d
          changeView(d.details.id, k)
        .on "mouseover", (d) ->
          tooltip.transition()
            .delay 100    
            .duration 100    
            .style 'opacity', .9
          # text =  dimensions.map( (dimension) -> "<div class='col-md-10 text-capitalize'>#{dimension}</div><div class='col-md-2'>#{d.details[dimension]}</div>").join('<br>')

          htmlText = "<table>" + dimensions.map( (dimension) ->
            "<tr><td class='text-capitalize'>#{dimension}</td><td><svg width='100' height='10'><rect width='#{parseFloat(d.details[dimension])*10}' height='10' fill='#c5e7ed'></rect></svg></td><td>#{d.details[dimension]}</td></tr>"
            ).join('') + "</table>"


          tooltip.html htmlText
          realW = tooltip.node().getBoundingClientRect().width

          fixedX = d3.event.pageX + 30
          if fixedX > $(window).width() / 2
            fixedX = d3.event.pageX - realW

          tooltip
            .style("left", "#{fixedX}px")
            .style("top", "#{d3.event.pageY}px")
        .on "mouseout", () ->
          tooltip.html('')
          tooltip.transition()
            .delay 100    
            .duration 100    
            .style 'opacity', 0

    g.append("path")
        .attr "d", (h) -> h.getSVGString()
        .attr "fill", (d) -> if d.details.id == focusId then "#c5e7ed" else "#ededed"
        # beautifeal color combination taken from http://www.nytimes.com/interactive/2016/06/24/world/europe/european-union-brexit-schengen-eurozone-nato.html
        .attr "id", (d) -> "#{d.r} #{d.q}"

    fo = g.append('foreignObject')
        .attr { 'width': hexW, 'height': hexH, 'class': 'hexagon-label' }
        .attr 'x', (d) -> d.x - hexW / 2
        .attr 'y', (d) -> d.y - hexH / 2

    fo.append('xhtml:div')
      .style 'height', hexH + "px"
    .append('div')
      .html (d) => "#{d.details.country}<br>#{d.details.region}"



$ ->
  k = 10
  focusId = Math.floor(Math.random() * 397)
  changeView focusId, k

