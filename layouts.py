# ── LAYOUT Item Reference ────────────────────────────────────────────────────
# Each item in LAYOUT is a dict with a "type" field and type-specific options.
#
# COMMON FIELDS
#   type          (str, required)  Element type. See options below.
#   name          (str, required)  Display label and base for the parameter name.
#   interactable  (bool)           Set False to disable interaction. Default: True
#
#
# TYPES
#
#   divider
#     Renders a full-width line of dashes. No other fields.
#     {"type": "divider"}
#
#   header
#     Renders a plain text title row. Not interactable.
#     {"type": "header", "name": "TINY UI"}
#
#   slider
#     A fill bar mapped to a float parameter. Click and drag to set value.
#     min      (float)  Minimum value. Default: 0.0
#     max      (float)  Maximum value. Default: 1.0
#     inverse  (bool)   Fills right-to-left instead of left-to-right. Default: False
#     {"type": "slider", "name": "amp", "min": 0.0, "max": 2.0, "inverse": False}
#
#   button
#     A pressable element backed by a Momentary or Toggle parameter.
#     btnStyle  (str)  "Momentary" fires while held, "Toggle" latches on/off.
#                      Default: "Momentary"
#     {"type": "button", "name": "pulse",  "btnStyle": "Momentary"}
#     {"type": "button", "name": "toggle", "btnStyle": "Toggle"}
#
#   radioButtons
#     A vertical list of exclusive options backed by a single Int parameter.
#     Clicking a row selects that index.
#     options  (list of str)  One row rendered per entry. Default: []
#     {"type": "radioButtons", "name": "mode", "options": ["sine", "square", "noise"]}
#
#   throbber
#     An animated spinner driven by a 0-1 float parameter. Display-only.
#     Drive it each frame: ext.UpdateThrobberVal("Phase", absTime.seconds % 1)
#     {"type": "throbber", "name": "phase"}
#
#   stringDisplay
#     A text readout backed by a string parameter. Display-only.
#     Update it: ext.UpdateStringVal("Perf", "120 fps")
#     {"type": "stringDisplay", "name": "perf"}
#
# ────────────────────────────────────────────────────────────────────────────

paramsLayout = [
		{"type": "header", "name": "TINY UI"},
		{"type": "divider"},
		{"type": "stringDisplay", "name": "FPS"},
		{"type": "slider", "name": "amp", "min": -1, "max": 1},
		{"type": "stringDisplay", "name": " "},
		{"type": "slider", "name": "warp"},
		{"type": "stringDisplay", "name": "   "},
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
		{"type": "slider", "name": "speed", "min": 0, "max": 1, "bipolar": True},
		{"type": "throbber", "name": "time", "interactable": False},
		{"type": "divider"},
		{"type": "radioButtons", "name": "InputSelect", "options": ["const", "low", "hi"]},
		{"type": "divider"},
		{"type": "button", "name": "reset", "btnStyle": "Momentary"},
		{"type": "divider"}
		]
		
clockDividerLayout = [
		{"type": "header", "name": "CLOCK DIVIDER"},
		{"type": "divider"},
		{"type": "button", "name": "tapTempo", "btnStyle": "momentary"},
		{"type": "stringDisplay", "name": "tempo"},
		{"type": "divider"},
		{"type": "radioButtons", "name": "inputSelect", "options": ["low", "high", "BPM"]},
		{"type": "divider"},
		{"type": "radioButtons", "name": "divs", "options": ["1/1", "2/1", "4/1", "8/1"]},
		{"type": "divider"},
		{"type": "button", "name": "sync", "btnStyle": "momentary"},
		{"type": "divider"},
		{"type": "button", "name": "output", "btnStyle": "momentary", "interactable": False},
		{"type": "divider"},
		

]
		
		
#op('tinyUI_parameters').SetLayout(paramsLayout)
#op('tinyUI_audioAnalysis').SetLayout(audioAnalysisLayout)
#op('tinyUI_timeKeeper').SetLayout(timeKeeperLayout)
op('tinyUI_clockDivider').SetLayout(clockDividerLayout)
