import re
from TDStoreTools import StorageManager
import TDFunctions as TDF

##TODO##
'''
-bind CHOP mapped to minMax 
'''
# ── Element type constants ───────────────────────────────────────────────────
T_SLIDER        = "slider"
T_BUTTON        = "button"
T_RADIO         = "radioButtons"
T_HEADER        = "header"
T_DIVIDER       = "divider"
T_THROBBER      = "throbber"
T_STRING        = "stringDisplay"

paramsLayout = [
		{"type": "header", "name": "TINY UI"},
		{"type": "divider"},
		{"type": "stringDisplay", "name": "FPS"},
		{"type": "slider", "name": "amp", "min": -1, "max": 1},
		{"type": "stringDisplay", "name": " "},
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


# ── Per-type handlers ────────────────────────────────────────────────────────
class _SliderHandler:
	def build_param(self, page, item, par_name):
		p           = page.appendFloat(par_name, label=item["name"])[0]
		p.min       = item.get("min", 0.0)
		p.max       = item.get("max", 1.0)
		p.normMin   = p.min
		p.normMax   = p.max
		p.clampMin  = True
		p.clampMax  = True
		p.default   = item.get("min", 0.0)
		p.val       = item.get("min", 0.0)

	def build_rows(self, ui, item, par_name):
		val     = ui._par_val(par_name, item.get("min", 0.0))
		inverse = item.get("inverse", False)
		return [(ui._fmt_name(item["name"]),
				ui._fmt_slider(val, inverse, item.get("min", 0.0), item.get("max", 1.0)))]

	def on_interact(self, ui, item, par_name, option_index):
		if not ui.Clicked:
			return
		sMin = item.get("min", 0.0)
		sMax = item.get("max", 1.0)
		val  = sMin + tdu.clamp(ui.InsideU, 0.0, 1.0) * (sMax - sMin)
		if hasattr(ui.ownerComp.par, par_name):
			ui.ownerComp.par[par_name].val = val
		ui.UpdateSliderVal(par_name, val)


class _ButtonHandler:
	def build_param(self, page, item, par_name):
		style = item.get("btnStyle", "Momentary")
		if style == "Toggle":
			page.appendToggle(par_name, label=item["name"])
		else:
			page.appendMomentary(par_name, label=item["name"])

	def build_rows(self, ui, item, par_name):
		pressed = ui.buttonState.get(par_name, False)
		return [(ui._fmt_name(item["name"]), ui._fmt_button(pressed))]

	def on_interact(self, ui, item, par_name, option_index):
		style = item.get("btnStyle", "Momentary")
		if style == "Toggle":
			if ui.Clicked:
				new_state = not ui.buttonState.get(par_name, False)
				ui.PressButton(par_name, new_state)
				if hasattr(ui.ownerComp.par, par_name):
					ui.ownerComp.par[par_name].val = 1 if new_state else 0
		else:
			ui.PressButton(par_name, ui.Clicked)
			if hasattr(ui.ownerComp.par, par_name):
				ui.ownerComp.par[par_name].val = 1 if ui.Clicked else 0


class _RadioHandler:
	def build_param(self, page, item, par_name):
		p          = page.appendInt(par_name, label=item["name"])[0]
		p.min      = 0
		p.max      = max(0, len(item.get("options", [])) - 1)
		p.clampMin = True
		p.clampMax = True
		p.default  = 0
		p.val      = 0

	def build_dummy_params(self, owner_comp, item, par_name):
		dummy_page = next(
			(p for p in owner_comp.customPages if p.name == "DUMMY PARS"), None
		)
		if dummy_page is None:
			dummy_page = owner_comp.appendCustomPage("DUMMY PARS")
		for i, opt in enumerate(item.get("options", [])):
			dummy_page.appendMomentary(f"{par_name}dummy{i}",
									label=f"{item['name']}dummy{i}")

	def build_rows(self, ui, item, par_name):
		sel     = int(ui._par_val(par_name, 0))
		options = item.get("options", [])
		return [(ui._fmt_menu_name(opt), ui._fmt_menu_val(i == sel))
				for i, opt in enumerate(options)]

	def on_interact(self, ui, item, par_name, option_index):
		if ui.Clicked:
			ui.SelectMenu(par_name, option_index)


class _ThrobberHandler:
	def build_param(self, page, item, par_name):
		p         = page.appendFloat(par_name, label=item["name"])[0]
		p.min     = 0.0
		p.max     = 1.0
		p.default = 0.0
		p.val     = 0.0

	def build_rows(self, ui, item, par_name):
		val = ui._par_val(par_name, 0.0)
		return [(ui._fmt_name(item["name"]), ui._fmt_throbber(val))]

	def on_interact(self, ui, item, par_name, option_index):
		pass  # throbbers are display-only


class _StringHandler:
	def build_param(self, page, item, par_name):
		p         = page.appendStr(par_name, label=item["name"])[0]
		p.default = ""
		p.val     = ""

	def build_rows(self, ui, item, par_name):
		val = ui._par_val(par_name, "")
		return [(ui._fmt_name(item["name"]), ui._fmt_string(str(val)))]

	def on_interact(self, ui, item, par_name, option_index):
		pass  # display-only


# Registry — maps type string → handler instance
_HANDLERS = {
	T_SLIDER:   _SliderHandler(),
	T_BUTTON:   _ButtonHandler(),
	T_RADIO:    _RadioHandler(),
	T_THROBBER: _ThrobberHandler(),
	T_STRING:   _StringHandler(),
}


# ── Main extension ───────────────────────────────────────────────────────────

class TDTinyUIExt:

	def __init__(self, ownerComp):
		self.ownerComp   = ownerComp
		self.outputTable = ownerComp.op("outputTable")
		self.sliderChar  = ownerComp.par.Slidercharacter.eval()
		self.emptyChar   = ownerComp.par.Emptycharacter.eval()
		self.buttonState = {}
		self.rowMap      = None
		self.armedForMidi = None

		##LAYOUT
		storedItems = [
			{'name': 'LAYOUT', 'default': paramsLayout, 'readOnly': False,
			'property': True, 'dependable': True},
		]
		self.stored = StorageManager(self, ownerComp, storedItems)

		TDF.createProperty(self, "SelectedRow", value=0,   dependable=True, readOnly=False)
		TDF.createProperty(self, "HoverRow",    value=0,   dependable=True, readOnly=False)
		TDF.createProperty(self, "InsideU",     value=0.0, dependable=True, readOnly=False)
		TDF.createProperty(self, "Clicked",     value=False, dependable=True, readOnly=False)

	# ── Helpers ──────────────────────────────────────────────────────────────

	def _par_val(self, par_name, default):
		"""Return ownerComp parameter value or a default if it doesn't exist."""
		if hasattr(self.ownerComp.par, par_name):
			return self.ownerComp.par[par_name].eval()
		return default

	@staticmethod
	def _parName(item):
		name = item.get("name", "").strip().lower().capitalize()
		name = re.sub("[^A-Za-z0-9]+", "", name)
		if not name or name[0].isnumeric():
			name = "Par" + name
		return name

	def _layout_dims(self):
		"""Return (MAX_CHARS, SLIDER_STEPS) cached for one method call."""
		return (
			self.ownerComp.par.Maxchars.eval(),
			self.ownerComp.par.Slidersteps.eval(),
		)

	# ── Formatting helpers ───────────────────────────────────────────────────

	def _fmt_name(self, name):
		MAX_CHARS, _ = self._layout_dims()
		name = name.replace(" ", self.emptyChar)
		return name[:MAX_CHARS].ljust(MAX_CHARS, self.emptyChar)

	def _fmt_slider(self, val, inverse=False, min=0.0, max=1.0):
		_, SLIDER_STEPS = self._layout_dims()
		normalized = tdu.clamp(
			(val - min) / (max - min) if max != min else 0.0, 0.0, 1.0
		)
		iVal = round(normalized * SLIDER_STEPS)
		if inverse:
			bar = self.emptyChar * iVal + self.sliderChar * (SLIDER_STEPS - iVal)
		else:
			bar = self.sliderChar * iVal + self.emptyChar * (SLIDER_STEPS - iVal)
		return "[" + bar + "]"

	def _fmt_button(self, pressed):
		return "[PUSH]" if pressed else "[    ]"

	def _fmt_menu_name(self, label):
		MAX_CHARS, _ = self._layout_dims()
		label = label.replace(" ", self.emptyChar)
		return label[:MAX_CHARS].ljust(MAX_CHARS, self.emptyChar)

	def _fmt_menu_val(self, selected):
		return f"[{self.sliderChar}]" if selected else "[ ]"

	def _fmt_throbber(self, val):
		FRAMES = ["|", "/", "-", "\\"]
		val    = tdu.clamp(val, 0.0, 1.0)
		index  = int(val * len(FRAMES)) % len(FRAMES)
		return f"[{FRAMES[index]}]"

	def _fmt_string(self, val):
		_, SLIDER_STEPS = self._layout_dims()
		val = str(val)[:SLIDER_STEPS]
		return "[" + val + "]"

	# ── Build helpers ────────────────────────────────────────────────────────

	def _buildParameters(self):
		for page_name in ("VALUES", "DUMMY PARS"):
			existing = next((p for p in self.ownerComp.customPages if p.name == page_name), None)
			if existing:
				existing.destroy()

		page = self.ownerComp.appendCustomPage("VALUES")

		for item in self.LAYOUT:
			t = item.get("type")
			handler = _HANDLERS.get(t)
			if handler is None:
				continue
			par_name = self._parName(item)
			handler.build_param(page, item, par_name)
			# Radio buttons also need dummy params for MIDI mapping
			if t == T_RADIO:
				handler.build_dummy_params(self.ownerComp, item, par_name)

	def _buildTable(self):
		self.outputTable.clear()
		self.outputTable.appendRow([])
		MAX_CHARS, SLIDER_STEPS = self._layout_dims()
		total_width = MAX_CHARS + SLIDER_STEPS + 2

		for item in self.LAYOUT:
			t = item.get("type")

			if t == T_DIVIDER:
				self.outputTable.appendRow(["-" * total_width, ""])
				continue

			if t == T_HEADER:
				self.outputTable.appendRow([item["name"], ""])
				continue

			handler = _HANDLERS.get(t)
			if handler is None:
				continue

			par_name = self._parName(item)
			for label, value in handler.build_rows(self, item, par_name):
				self.outputTable.appendRow([label, value])

		if self.outputTable[0, 0] == "":
			self.outputTable.deleteRow(0)

	def _buildRowMap(self):
		row_map = []
		for item in self.LAYOUT:
			t = item.get("type")
			if t == T_RADIO:
				for i in range(len(item.get("options", []))):
					row_map.append((item, i))
			else:
				row_map.append((item, None))
		return row_map

	def _buildRowIndex(self):
		"""Reverse lookup: (id(item), option_index) -> table row number."""
		index = {}
		row = 0
		for item in self.LAYOUT:
			t = item.get("type")
			if t == T_RADIO:
				for i in range(len(item.get("options", []))):
					index[(id(item), i)] = row
					row += 1
			else:
				index[(id(item), None)] = row
				row += 1
		return index

	def _getTableRow(self, target_item, target_option=None):
		return self._rowIndex.get((id(target_item), target_option))

	def _buildComponent(self):
		fontSize   = self.ownerComp.par.fontsize.eval()
		numRows    = self.outputTable.numRows
		MAX_CHARS, SLIDER_STEPS = self._layout_dims()
		totalCols  = MAX_CHARS + SLIDER_STEPS + 2
		charAspect = 0.6
		rowPadding = 1.2
		self.ownerComp.par.w.val = fontSize * charAspect * totalCols
		self.ownerComp.par.h.val = fontSize * numRows * rowPadding

	def _isInteractable(self, item):
		return item.get("interactable", True)

	def _setup(self):
		self.sliderChar  = self.ownerComp.par.Slidercharacter.eval()
		self.emptyChar   = self.ownerComp.par.Emptycharacter.eval()
		self.buttonState = {}
		self._buildParameters()
		self._buildTable()
		self.rowMap    = self._buildRowMap()
		self._rowIndex = self._buildRowIndex()
		self._buildComponent()
		op("postSetUp").run()

	# ── Public API ───────────────────────────────────────────────────────────

	def GetParName(self, name):
		return self._parName({"name": name})

	def UpdateSliderVal(self, par_name, val):
		for item in self.LAYOUT:
			if item.get("type") == T_SLIDER and self._parName(item) == par_name:
				row = self._getTableRow(item)
				if row is not None:
					self.outputTable[row, 1] = self._fmt_slider(
						val,
						item.get("inverse", False),
						item.get("min", 0.0),
						item.get("max", 1.0),
					)
				return

	def PressButton(self, par_name, val):
		self.buttonState[par_name] = bool(val)
		for item in self.LAYOUT:
			if item.get("type") == T_BUTTON and self._parName(item) == par_name:
				row = self._getTableRow(item)
				if row is not None:
					self.outputTable[row, 1] = self._fmt_button(bool(val))
				return

	def SelectMenu(self, par_name, index):
		if hasattr(self.ownerComp.par, par_name):
			self.ownerComp.par[par_name].val = index
		for item in self.LAYOUT:
			if item.get("type") == T_RADIO and self._parName(item) == par_name:
				options = item.get("options", [])
				index   = int(tdu.clamp(index, 0, len(options) - 1))
				for i in range(len(options)):
					row = self._getTableRow(item, i)
					if row is not None:
						self.outputTable[row, 1] = self._fmt_menu_val(i == index)
				return

	def GetRowInfo(self, row):
		if row is None or self.rowMap is None or row >= len(self.rowMap):
			return None
		item, option_index = self.rowMap[row]
		t       = item.get("type")
		name    = item.get("name", "")
		par_name = self._parName(item) if t not in (T_DIVIDER, T_HEADER) else None
		return (t, name, par_name, option_index)

	def UpdateFromPanel(self, fromClick=False):
		info = self.GetRowInfo(self.SelectedRow)
		if info is None:
			return
		t, name, par_name, option_index = info

		item = next((i for i in self.LAYOUT if i.get("name") == name), None)
		if item is None or not self._isInteractable(item):
			return

		handler = _HANDLERS.get(t)
		if handler is None:
			return

		if t == T_BUTTON and not fromClick:
			return  # buttons only fire on click

		handler.on_interact(self, item, par_name, option_index)

	def UpdateThrobberVal(self, par_name, val):
		for item in self.LAYOUT:
			if item.get("type") == T_THROBBER and self._parName(item) == par_name:
				row = self._getTableRow(item)
				if row is not None:
					self.outputTable[row, 1] = self._fmt_throbber(val % 1)
				return

	def UpdateStringVal(self, par_name, val):
		for item in self.LAYOUT:
			if item.get("type") == T_STRING and self._parName(item) == par_name:
				row = self._getTableRow(item)
				if row is not None:
					self.outputTable[row, 1] = self._fmt_string(str(val))
				return

	def SetLayout(self, layout):
		self.LAYOUT = layout
		self._setup()
		
	def GetSelectedPar(self):
		pName = self.GetRowInfo(self.SelectedRow)[2]
		p = self.ownerComp.par[pName]
		return p

	def UpdateComponent(self):
		self._buildComponent()

	# ── MIDI mapping ─────────────────────────────────────────────────────────

	def MidiMap(self, remove=False):
		if not hasattr(op, "tinyUI_midiMapper"): return
		if not op.tinyUI_midiMapper.par.Midimap: return
	
		info = self.GetRowInfo(self.SelectedRow)
		if info is None:
			return
		t, name, par_name, option_index = info
	
		item = next((i for i in self.LAYOUT if i.get("name") == name), None)
		if item is None or not self._isInteractable(item):
			return
	
		target_par = (
			f"{par_name}dummy{option_index}"
			if (t == T_RADIO and option_index is not None)
			else par_name
		)
		if remove:
			self.armedForMidi = None
			self.ownerComp.par[target_par].bindExpr = ""
			return
		self.armedForMidi = target_par
	
		op.tinyUI_midiMapper.IncomingPar = self.ownerComp.par[target_par]
		return

	def WhenMidiChanges(self, midi_chan):
		if self.armedForMidi is None:
			return
		self.ownerComp.par[self.armedForMidi].bindExpr = f"op('./bind1')['{midi_chan}']"
		self.armedForMidi = None

	# ── Init ─────────────────────────────────────────────────────────────────

	def onInitTD(self):
		self._setup()