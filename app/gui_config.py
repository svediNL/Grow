## G U I   D E S I G N
try:
    from Tkinter import font
except:
    from tkinter import font


THEME_DARK		= False

if THEME_DARK:
	BG_MAIN			= "gray30"
	BG_SUB 			= "gray33"
	BG_SUBSUB 		= "white"
	BG_TOG_A		= BG_SUB
	BG_TOG_B 		= "gray44"
	BG_TAB 			= "gray44"
	BG_TAB_ACTIVE 	= BG_SUB
	BG_ENTRY		= "gray60"
	BG_BUTTON		= "black"
	BG_CHECK		= "gray40"
	BG_SEL   		= "gray77"

	FG_TEXT			= "white"
	FG_TEXT2		= "black"
	FG_ENTRY		= "white"

else:
	BG_MAIN			= "gray93"
	BG_SUB 			= "gray96"
	BG_SUBSUB 		= "white"
	BG_TOG_A		= "gray96"
	BG_TOG_B 		= "gray93"
	BG_TAB 			= "gray85"
	BG_TAB_ACTIVE 	= "gray96"
	BG_ENTRY		= "white"
	BG_BUTTON		= "black"
	BG_CHECK		= "gray40"
	BG_SEL   		= "gray77"

	FG_TEXT			= "black"
	FG_TEXT2		= "black"
	FG_ENTRY		= "white"


FONT_DEFAULT = font.nametofont("TkDefaultFont") # load default
FONT_DEFAULT.configure( #
	family = "Courier",#
	size = -14,
	weight = font.NORMAL)

#FONT_TITLE = 
font.Font(
	name = "Title",
	family = "Courier", 
	size = -18, 
	weight = font.BOLD)


THERMO_PLOT_CMAP = ['r', 'g', 'b', 'm', 'k']
MOIST_PLOT_CMAP = ['r', 'g', 'b', 'm', 'k']
PUMP_PLOT_CMAP = ['r', 'g', 'b', 'm', 'k']
LIGHT_PLOT_CMAP = ['r', 'g', 'b', 'm', 'k']