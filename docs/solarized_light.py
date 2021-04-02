C_TEXT='#586E75'
#C_TEXT(BOLD)='#586E75'
C_BACKGROUND='#FDF6E3'
C_BLACK='#002B36'
#C_BLACK(BOLD)='#657B83'
C_RED='#DC322F'
#C_RED(BOLD)='#DC322F'
C_GREEN='#859900'
#C_GREEN(BOLD)='#859900'
C_YELLOW='#B58900'
#C_YELLOW(BOLD)='#B58900'
C_BLUE='#268BD2'
#C_BLUE(BOLD)='#268BD2''
C_MAGENTA='#6C71C4'
#C_MAGENTA(BOLD)='#6C71C4'
C_CYAN='#2AA198'
#C_CYAN(BOLD)='#2AA198'
PYLOAD={'fontcolor':C_YELLOW,'color':C_BLACK,'style':'filled','fillcolor':"#FFFFFF", 'fontname':'qwer'}
DBSTORE={'fontcolor':C_MAGENTA,'color':C_BLACK,'style':'filled','fillcolor':C_BACKGROUND, 'fontname':'NotoMono'}
OPERATOR={'fontcolor':C_BLACK,'color':C_BLACK,'style':'filled','fillcolor':C_BACKGROUND, 'fontname':'NotoMono'}
DBLOAD={'fontcolor':C_RED,'color':C_BLACK,'style':'filled','fillcolor':C_BACKGROUND, 'fontname':'NotoMono'}
PYSTORE={'fontcolor':C_BLUE,'color':C_BLACK,'style':'filled', 'fillcolor':'#FFFFFF', 'fontname':'NotoMono'}
ACTION={'fontcolor':C_BLACK,'color':C_BLACK,'style':'filled', 'fillcolor':'#FFFFFF', 'fontname':'NotoMono'}

def TO(node, TYPE):
    for key, value in TYPE.items():
        node[key]=value
    return node