background_col = "rgb(51, 51, 51)"
acient_col = "rgb(86, 186, 150)"
acient_col2 = "rgb(172, 255, 255)"


sheets = {
"task":
"""
QLabel {{
    text-align: right;
    font-size: 15px;
    background : {0};
    color : {1};        
}}
QLabel:hover {{
    color : {2};  
          
}}
""".format(background_col, acient_col, acient_col2),
"account":
"""
QLabel {{
    font-size: 15px;
    background : {0};
    color : {1};        
}}
QLabel:hover {{
    color : {2};        
}}
""".format(background_col, acient_col, acient_col2),

"window":
"""
background : {0};
color : {1};
""".format(background_col, acient_col, acient_col2),
"table":
"""
border:0;
""".format(background_col, acient_col, acient_col2),
"00":
"""
font-size: 15px;
color: {1}
""".format(background_col, acient_col, acient_col2),
"table_button":
"""
QPushButton#new_task {{
    width: 70px;
    height: 40px;
    font-size: 15px;
    margin-left: 10px;
    color: {1};
    outline: none;
    background: transparent;
}}
QPushButton#new_task:hover {{
    color: {2};
}}
QPushButton {{
    width: 80px;
    height: 40px;
    font-size: 15px;
    color: {1};
    outline: none;
    background: transparent;
}}
QPushButton:hover {{
    color: {2};
}}
  
  
""".format(background_col, acient_col, acient_col2),

}
def get_style(name):
    if (name != "window"):
        return ""
    print(sheets[name])
    return sheets[name]