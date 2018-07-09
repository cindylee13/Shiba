              function Minus()
              {
                var svg = d3.select("svg");
                var paths = svg.selectAll('.lineask').attr("first");
                var id = d3.select('svg').attr('id');
                var pathData = [];
                timedelta=5*60*1000
                firstTime=new Date(paths)
                data=all[id]
                $.each(data, function(index, value) {
                    if(value.date-firstTime >= timedelta)
                      pathData.push(value);
                }); 

                draw(pathData,id,new Date(firstTime.getTime()+timedelta));
              }
              function Plus()
              {
                var paths = svg.select('.lineask').attr("first");
                var id = d3.select('svg').attr('id');
                timedelta=5*60*1000
                data=all[id];
                g=paths._groups
                firstTime=new Date(paths)
                var pathData = [];
                data.map(Obj => {
                  if(firstTime - Obj.date <= timedelta)
                    pathData.push(Obj);
                  });
                draw(pathData,id,new Date(firstTime.getTime()-timedelta));
              }
              function mousemove() {
                  var x0 = x.invert(d3.mouse(this)[0]),
                      i = bisectDate(data, x0, 1),
                      d0 = data[i - 1],
                      d1 = data[i],
                      d = x0 - d0.date > d1.date - x0 ? d1 : d0;
                  focus.attr("transform", "translate(" + x(d.date) + "," + y(d.closeBid) + ")");
                  focus.select("text").text('('+d.date+','+formatCurrency(d.closeBid)+','+formatCurrency(d.closeAsk)+')');
              }
              function draw(data,transection,firstTime)
              {
                  svg = d3.select("svg");//.transition();
                  x.domain([data[0].date, data[data.length - 1].date]);
                  y.domain(d3.extent(data, function(d) { return d.closeBid; }));
                  y1.domain(d3.extent(data, function(d) { return d.closeAsk; }));
                  var line = d3.line()
                      .x(function(d) { return x(d.date); })
                      .y(function(d) { return y(d.closeBid); });
                  var lineAsk = d3.line()
                      .x(function(d) { return x(d.date); })
                      .y(function(d) { return y1(d.closeAsk); });
                  svg.attr("id",transection);
                  svg.select('.xaxis').call(d3.axisBottom(x)
                    .tickFormat(d3.timeFormat("%H:%M:%S")));
                  svg.select('.date').call(d3.axisTop(x)
                    .tickFormat(d3.timeFormat("%y-%m-%d")));
                  svg.select(".linebid").transition()   // change the line
                     //.duration(750)
                     .attr("d", line(data))
                     .attr("first",firstTime);
                  svg.data(data);
                  svg.select(".lineask").transition()   // change the line
                     //.duration(750)
                     .attr("d", lineAsk(data))
                     .attr("first",firstTime);
                  svg.select(".x.axis").transition() // change the x axis
                      //.duration(750)
                      .call(x);
                  svg.select(".y.axis").transition() // change the y axis
                      //.duration(750)
                      .call(y);
                  svg.select(".y1.axis").transition() // change the y axis
                      //.duration(750)
                      .call(y1);

                  //svg.duration(4000).transition();

              }
              function getDate(transectionName)
              {
                firsttime=all[transectionName][0].date
                //console.log("all="+all)
                draw(all[transectionName],transectionName,firsttime)
              }