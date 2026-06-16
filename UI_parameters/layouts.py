paramsLayout = [
		{"type": "header", "name": "TINY UI"},
		{"type": "divider"},
		{"type": "stringDisplay", "name": "FPS"},
		{"type": "slider", "name": "amp"},
		{"type": "slider", "name": "warp"},
		{"type": "slider", "name": "scale"},
		{"type": "divider"},
		{"type": "button", "name": "toggle", "btnStyle": "Toggle"},
		{"type": "button", "name": "pulse", "btnStyle": "Momentary"},
		{"type": "divider"},
		{"type": "radioButtons", "name": "mode", "options": ["sine", "square", "noise", "test"]},
		{"type": "divider"},
		{"type": "slider", "name": "spin"},
		{"type": "divider"},
		{"type": "radioButtons", "name": "radfioBtn", "options": ["sine", "square", "noise", "test"]},
		{"type": "slider", "name": "smth"},
		{"type": "divider"},
		{"type": "throbber", "name": "phase"},
		{"type": "divider"}
		]
		
audioAnalysisLayout = [
		{"type": "header", "name": "AUDIO ANALYSIS"},
		{"type": "divider"},
		
		{"type": "slider", "name": "low", "interactable": False},
		{"type": "slider", "name": "thrL", "interactable": True, "inverse": True},
		{"type": "button", "name": "lowTrig", "btnStyle": "Momentary", "interactable": False},
		
		{"type": "divider"},
		{"type": "slider", "name": "hi", "interactable": False},
		{"type": "slider", "name": "thrH", "interactable": True, "inverse": True},
		
		{"type": "button", "name": "hiTrig", "btnStyle": "Momentary", "interactable": False},
		{"type": "divider"},
		{"type": "slider", "name": "vol"},
		{"type": "divider"}
		]
		
timeKeeperLayout = [
		{"type": "header", "name": "TIME KEEPER"},
		{"type": "divider"},
		{"type": "slider", "name": "speed"},
		{"type": "throbber", "name": "time"},
		{"type": "divider"},
		{"type": "radioButtons", "name": "Inputs", "options": ["const", "low", "hi"]},
		{"type": "divider"}
		]
		
