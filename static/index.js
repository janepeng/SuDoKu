// some globals..
var oldrow = -1;
var oldcol = -1;

function createTable() {
    var num_rows = 9;
    var num_cols = 9;
    var theader = '<table border="1" id="game_table">\n';
    var tbody = '<tbody class="table table-hover">\n';

    for (var i = 0; i < num_rows; i++)
    {
        tbody += '<tr ';
        if (i % 3 == 2) {
            tbody += 'class="edge_row" ';
        }
        tbody += '>';
        for (var j = 0; j < num_cols; j++)
        {
            tbody += '<td ';
            if (j % 3 == 2) {
                tbody += 'class="edge_col ' + i + j + '"';
            } else {
                tbody += 'class="' + i + j + '"';
            }
            tbody += '>\n';
            tbody += '<input onclick="highlightRowCol(this)" name="' + i + j + '" size="1" autocomplete="off" maxlength="1" class="input_box ' + i + j +'">';
            tbody += '</td>';
        }
        tbody += '</td>\n';
    }
    tbody += '</tbody>';
    var tfooter = '</table>';
    document.getElementById('game_board').innerHTML = theader + tbody + tfooter;
}

function createResultTable(input) {
    var num_rows = 9;
    var num_cols = 9;
    var theader = '<table border="1" id="result_table">\n';
    var tbody = '<tbody class="table table-hover">\n';
    var board = input.split(" ");
    var ctr = 0;

    for (var i = 0; i < num_rows; i++)
    {
        tbody += '<tr ';
        if (i % 3 == 2) {
            tbody += 'class="edge_row" ';
        }
        tbody += '>';
        for (var j = 0; j < num_cols; j++)
        {
            tbody += '<td valign="middle" ';
            if (j % 3 == 2) {
                tbody += 'class="edge_col ' + i + j + '"';
            } else {
                tbody += 'class="' + i + j + '"';
            }
            tbody += '>\n';
            tbody += '<p>' + board[ctr] + '</p>';
            tbody += '</td>';
        }
        tbody += '</td>\n';
    }
    tbody += '</tbody>';
    var tfooter = '</table>';
    document.getElementById('result_board').innerHTML = theader + tbody + tfooter;
}

function clearTable(rows, cols, row, col) {
    rows[row].classList.remove("highlighted");
    var j = 0;
    for (i = 0; i < cols.length; i++) {
        var rowcol = j.toString() + col.toString();
        if (cols[i].className.indexOf(rowcol) > -1) {
            cols[i].classList.remove("highlighted");
            j++;
        }
    }
} 

function highlightRowCol(cell) {
    var row = parseInt(cell.classList[1].charAt(0));
    var col = parseInt(cell.classList[1].charAt(1));
    var table = document.getElementById('game_table');
    var rows = table.getElementsByTagName('tr');
    var cols = table.getElementsByTagName('td');
    if (oldrow != -1) {
        clearTable(rows, cols, oldrow, oldcol);
    }
    rows[row].className += " highlighted";
    var j = 0;
    for (i = 0; i < cols.length; i++) {
        var rowcol = j.toString() + col.toString();
        if (cols[i].className.indexOf(rowcol) > -1) {
            cols[i].className += " highlighted";
            j++;
        }
    }
    oldrow = row;
    oldcol = col;
}

$(document).ready(function() {
    console.log("ready!");
    createTable();
    $('form').bind('submit', function(e) {
        jQuery.ajax({
            url: '/submit',
            type: 'POST',
            data: null,
            success: function(data) {
                createResultTable(data); 
            }
        });
        e.preventDefault();
        return false;
    });
});
