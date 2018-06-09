var dynamicTable = (function() {
          var _tableId, _table,
          _fields, _headers,
          _defaultText;
          function UpdateTable(transectionId)
          {
            a=document.getElementById('Cex')
          }
          function AddRow(item,names)
          {
            table = document.getElementById("dataTable");
            var row = table.insertRow(table.length);
            row.id=item['transection'];
            var i=0;
            names=names.reverse()
            $.each(names, function(index, name) {
              var cell1 = row.insertCell(i);
              cell1.innerHTML = item[name+''];
            });
          }
          function Update(item,names)
          {
            table = document.getElementById(item['transection']);
            var i=0
            //names=names.reverse()
            $.each(names, function(index, name) {
              table.cells[i].innerHTML=item[name+'']
              i++
            });
            //table.innerHTML
          }
          function _buildRowColumns(names, item) {
            var row=''
            if(item)
            {
              if(document.getElementById(item['transection'])==null)
                AddRow(item,names)
              
              else
                Update(item,names)       
              return ''
            }
            else
            {
              row='<tr>'
              $.each(names, function(index, name) {
              var c = item ? item[name+''] : name;
              row += '<td>' + c + '</td>';
              });
              row += '</tr>';
            }
            return row;
          }


          return {
            //* Configres the dynamic table.
            config: function(tableId, fields, headers, defaultText) {
              _tableId = tableId;
              _table = $(document.getElementById(_tableId))//$('#' + tableId);
              _fields = fields || null;
              _headers = headers || null;
              _defaultText = defaultText || 'No items to list...';
              //_setHeaders();
              return this;
                    },
            /** Loads the specified data to the table body. */
            load: function(data, append) {
              var i=0;
                //transectionId=data[0]['transection']
                //console.log(data.length)
                if (data && data.length > 0) {
                  var rows = '';
                  $.each(data, function(index, item) {
                    rows += _buildRowColumns(_fields, item);
                  });

                  var mthd = append ? 'append' : 'html';
                  if(rows!='')
                    _table.children('tbody')[mthd](rows);
                  }
                return this;
          },
              /** Clears the table body. */
        };
        }());