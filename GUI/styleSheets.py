background_col = "rgb(51, 51, 51)"
accent_col = "rgb(86, 186, 150)"
accent_col2 = "rgb(172, 255, 255)"


sheets = {
"main":
"""
QPushButton{{
background : {0};
color : {1};
font-size: 15px;
min-width: 40px;
padding-left: 20px;
padding-right: 20px;
border-radius: 10px; 
}}

QPushButton:hover{{
background : {1};
color : {2};
}}

QLabel {{
font-size : 15px;
padding-left: 30px;
padding-right: 20px;
background : {0};
color : {1};
}}

QLabel#item:hover {{
color : {2};
}}

QLabel#heading {{
font-size : 20px;
}}

QTableView{{
background: {0};
border: 0;
}}

QMainWindow {{
background: {0};
}}

QDialog {{
background: {0};
}}

QLineEdit {{
qproperty-frame: false;
border: solid 1;
border-color: white;
background : {0};
color : {1};
}}

QTextBrowser {{
background: {0};
color: {1};
border-color: {1}
}}

""".format(background_col, accent_col, accent_col2),

"popups":
"""
QMainWindow {{
background: {0};
}}

QLabel {{
color : {1};
font-size: 20;
}}

QTextBrowser {{
background: {0};
color: {1};
border-color: {1}
}}
""".format(background_col, accent_col, accent_col2),

}
def get_style(name):
    print(sheets[name])
    return sheets[name]