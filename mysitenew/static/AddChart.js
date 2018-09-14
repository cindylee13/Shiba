margin = {top: 20, right: 50, bottom: 30, left: 50},
                width = 960 - margin.left - margin.right,
                height = 500 - margin.top - margin.bottom;
              var svg = d3.select("svg").append("svg")
                  .attr("width", width + margin.left + margin.right)
                  .attr("height", height + margin.top + margin.bottom)
                  .append("g")
                  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
              //var parseTime = d3.timeParse("%Y-%m-%d %H:%M:%S");
              bisectDate = d3.bisector(function(d) { return d.date; }).left,
              formatValue = d3.format(",.2f"),
              formatCurrency = function(d) { return "$" + formatValue(d); };
              var x = d3.scaleTime()
                  .range([0, width]);

              var y = d3.scaleLinear()
                  .range([height, 0]);
              var y1 = d3.scaleLinear()
                  .range([height, 0]);

              var yAxis = d3.axisLeft()
                  .scale(y)
              var yAxis1 = d3.axisLeft()
                  .scale(y1)

              var line = d3.line()
                  .x(function(d) { return x(d.date); })
                  .y(function(d) { return y(d.closeBid); });

              var lineAsk = d3.line()
                  .x(function(d) { return x(d.date); })
                  .y(function(d) { return y1(d.closeAsk); });

                data.sort(function(a, b) {
                  return a.date - b.date;
                });
              console.log(data)
              //draw(data,true)
                x.domain([data[0].date, data[data.length - 1].date]);
                y.domain(d3.extent(data, function(d) { return d.closeBid; }));
                y1.domain(d3.extent(data, function(d) { return d.closeAsk; }));

                svg.append("g")
                    .attr("class", "xaxis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(d3.axisBottom(x)
                    .tickFormat(d3.timeFormat("%H:%M:%S")));


                svg.append("g")
                    .attr("class", "date")
                    .attr("transform", "translate(0," + height + ")")
                    .call(d3.axisTop(x)
                    .tickFormat(d3.timeFormat("%y-%m-%d")));


                svg.append("g")
                    .attr("class", "yaxis")
                    .call(yAxis)
                  .append("text")
                  .attr("fill", "#000")
                    .attr("transform", "rotate(-90)")
                    .attr("y", 6)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text("Price ($)");

                svg.append("g")
                    .attr("class", "y1 axis")
                    .attr("transform", "translate(" + width + " ,0)")
                    .style("fill", "red")
                    .call(y1);

                svg.append("path")
                    //.data(data)
                    .attr("fill", "none")
                    .attr("stroke", "#CC00CC")
                    .attr("stroke-linejoin", "round")
                    .attr("stroke-linecap", "round")
                    .attr("stroke-width", 1.5)
                    .attr("class", "linebid")
                    .attr("first",data[0].date)
                    .attr("d", line(data));
//console.log("======="+all['Bittrex'][0].date)
                svg.append("path")
                    //.data(data)
                    .attr("fill", "none")
                    .attr("stroke", "steelblue")
                    .attr("stroke-linejoin", "round")
                    .attr("stroke-linecap", "round")
                    .attr("stroke-width", 1.5)
                    .attr("class", "lineask")
                    .attr("first",data[0].date)
                    .attr("d", lineAsk(data));

                var focus = svg.append("g")
                    .attr("class", "focus")
                    .attr("fill", "none")
                    .attr("stroke", "steelblue")
                    .style("display", "none");
                focus.append("circle")
                    .attr("r", 1);

                focus.append("text")
                    .attr("x", 9)
                    .attr("dy", ".1em");

                svg.append("rect")
                    .attr("class", "overlay")
                    .attr("fill", "none")
                    .attr("pointer-events", "all")
                    .attr("width", width)
                    .attr("height", height)
                    .on("mouseover", function() { focus.style("display", null); })
                    .on("mouseout", function() { focus.style("display", "none"); })
                    .on("mousemove", mousemove);