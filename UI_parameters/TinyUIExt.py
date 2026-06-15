

from TDStoreTools import StorageManager
import TDFunctions as TDF

class TDTinyUIExt:
	"""
	#set the parameters up by filling out the LAYOUT dictionary
	
		type: header, name: "something"
		type: divider 
		type: slider, name: "something"
		type: button: name: "somethinhg", btnStyle: "Toggle" or "Momentary"
		type: radioButtons, name: "something", "options": [list of btn labels]
	"""
	LAYOUT = [

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

	
	def __init__(self, ownerComp):
		self.ownerComp   = ownerComp
		self.outputTable = ownerComp.op('outputTable')
		self.sliderChar  = ownerComp.par.Slidercharacter.eval()
		self.emptyChar   = ownerComp.par.Emptycharacter.eval()
		self.buttonState = {} 
		self.rowMap = None
		self.armedForMidi = None


		
		#-----PANEL INTERACTION---##
		TDF.createProperty(self, 'SelectedRow', value=0,  dependable=True, readOnly=False)
		TDF.createProperty(self, 'HoverRow',    value=0,  dependable=True, readOnly=False)
		TDF.createProperty(self, 'InsideU',     value=0.0,dependable=True, readOnly=False)
		TDF.createProperty(self, 'Clicked',     value=False, dependable=True, readOnly=False)
		
		#------LAYOUT MATH-----#
		

	def _parName(self, item):
	    name = item["name"].strip().lower().capitalize()
	    name = re.sub('[^A-Za-z0-9]+', '', name)
	    if not name or name[0].isnumeric():
	        name = 'Par' + name
	    return name
		
	def _buildParameters(self):
		for pageName in ('VALUES', 'DUMMY PARS'):
			existingPage = next((p for p in self.ownerComp.customPages if p.name == pageName), None)
			if existingPage:
				existingPage.destroy()
	
		page = self.ownerComp.appendCustomPage('VALUES')

		for item in self.LAYOUT:
			t = item.get("type")
			if t == "divider":
				continue

			parName = self._parName(item)

			if t == "slider":
				p = page.appendFloat(parName, label=item["name"])[0]
				p.min      = 0.0
				p.max      = 1.0
				p.clampMin = True
				p.clampMax = True
				p.default  = 0.0
				p.val      = 0.0

			elif t == "button":
				btnStyle = item.get("btnStyle", "Momentary")
				if btnStyle == "Toggle":
					page.appendToggle(parName, label=item["name"])
				else:
					page.appendMomentary(parName, label=item["name"])

			elif t == "radioButtons":
				p = page.appendInt(parName, label=item["name"])[0]
				p.min      = 0
				p.max      = max(0, len(item.get("options", [])) - 1)
				p.clampMin = True
				p.clampMax = True
				p.default  = 0
				p.val      = 0
				
				dummyPage = next((p for p in self.ownerComp.customPages if p.name == 'DUMMY PARS'), None)
				if dummyPage is None:
					dummyPage = self.ownerComp.appendCustomPage('DUMMY PARS')
			
				for i, opt in enumerate(item.get("options", [])):
					dummyParName = f"{parName}dummy{i}"
					dummyPage.appendMomentary(dummyParName, label=f"{item['name']}dummy{i}")
			
			elif t == "throbber":
				p = page.appendFloat(parName, label=item["name"])[0]
				p.min      = 0.0
				p.max      = 1.0
				#p.clampMin = True
				#p.clampMax = True
				p.default  = 0.0
				p.val      = 0.0
				
			elif t == "stringDisplay":
				p = page.appendStr(parName, label=item["name"])[0]
				p.default = ""
				p.val = ""
			

	def _buildTable(self):
		self.outputTable.clear()
		self.outputTable.appendRow([])

		for item in self.LAYOUT:
			t = item.get("type")

			if t == "divider":
				MAX_CHARS    = self.ownerComp.par.Maxchars.eval()
				SLIDER_STEPS = self.ownerComp.par.Slidersteps.eval()
				divChar      = "-"
				totalWidth   = MAX_CHARS + SLIDER_STEPS + 2
				self.outputTable.appendRow([divChar * totalWidth, ""])

			elif t == "slider":
				parName  = self._parName(item)
				val      = self.ownerComp.par[parName].eval() if hasattr(self.ownerComp.par, parName) else 0.0
				inverse  = item.get("inverse", False)
				self.outputTable.appendRow([
					self._getSliderName(item["name"]),
					self._getSliderVal(val, inverse=inverse),
				])

			elif t == "button":
				parName = self._parName(item)
				pressed = self.buttonState.get(parName, False)
				self.outputTable.appendRow([
					self._getSliderName(item["name"]),
					self._getButtonVal(pressed),
				])

			elif t == "header":
				MAX_CHARS    = self.ownerComp.par.Maxchars.eval()
				SLIDER_STEPS = self.ownerComp.par.Slidersteps.eval()
				totalWidth   = MAX_CHARS + SLIDER_STEPS + 2
				text         = item["name"]
				self.outputTable.appendRow([text, ""])

			elif t == "radioButtons":
				parName  = self._parName(item)
				selIndex = int(self.ownerComp.par[parName].eval()) if hasattr(self.ownerComp.par, parName) else 0
				options  = item.get("options", [])
				# One row per option
				for i, opt in enumerate(options):
					self.outputTable.appendRow([
						self._getMenuOptionName(opt),
						self._getMenuOptionVal(i == selIndex),
					])
					
			elif t == "throbber":
				parName = self._parName(item)
				val     = self.ownerComp.par[parName].eval() if hasattr(self.ownerComp.par, parName) else 0.0
				self.outputTable.appendRow([
					self._getSliderName(item["name"]),
					self._getThrobberVal(val),
				])
				
			elif t == "stringDisplay":
				parName = self._parName(item)
				val = self.ownerComp.par[parName].eval() if hasattr(self.ownerComp.par, parName) else ""
				self.outputTable.appendRow([
					self._getSliderName(item["name"]),
					self._getStringVal(val),
				])

		if self.outputTable[0, 0] == "":
			self.outputTable.deleteRow(0)
			
	def _isInteractable(self, item):
		return item.get("interactable", True)

	# ── Formatting helpers ──────────────────────────────────────────────────

	def _getSliderName(self, name):
		MAX_CHARS = self.ownerComp.par.Maxchars.eval()
		name = name.replace(" ", self.emptyChar)
		return name[:MAX_CHARS].ljust(MAX_CHARS, self.emptyChar)

	def _getSliderVal(self, val, inverse = False):
		val          = tdu.clamp(val, 0.0, 1.0)
		SLIDER_STEPS = self.ownerComp.par.Slidersteps.eval()
		iVal         = round(val * SLIDER_STEPS)
		
		if inverse:
			bar = self.emptyChar * iVal + self.sliderChar * (SLIDER_STEPS - iVal)
		else:
			bar = self.sliderChar * iVal + self.emptyChar * (SLIDER_STEPS - iVal)
		
		return "[" + bar + "]"

	def _getButtonVal(self, pressed):
		if pressed:
			return f"[PUSH]"
		return     "[    ]"

	def _getMenuOptionName(self, label):
		MAX_CHARS = self.ownerComp.par.Maxchars.eval()
		label     = label.replace(" ", self.emptyChar)
		full      = (label)[:MAX_CHARS]
		return full.ljust(MAX_CHARS, self.emptyChar)

	def _getMenuOptionVal(self, selected):
		if selected:
			return f"[{self.sliderChar}]"
		return     "[ ]"
		
	def _getThrobberVal(self, val):
		FRAMES = ['|', '/', '-', '\\']
		val    = tdu.clamp(val, 0.0, 1.0)
		index  = int(val * len(FRAMES)) % len(FRAMES)
		return f"[{FRAMES[index]}]"
		
	def _buildRowMap(self):
		rowMap = []
		for item in self.LAYOUT:
			t = item.get("type")
			if t == "radioButtons":
				for i, _ in enumerate(item.get("options", [])):
					rowMap.append((item, i))
			else:
				rowMap.append((item, None))
		return rowMap


	def _getTableRow(self, targetItem, targetOptionIndex=None):
		row = 0
		for item in self.LAYOUT:
			t = item.get("type")
			if item is targetItem:
				if t == "radioButtons" and targetOptionIndex is not None:
					return row + targetOptionIndex
				return row
			if t == "radioButtons":
				row += len(item.get("options", []))
			else:
				row += 1
		return None
		
	def _getStringVal(self, val):
		SLIDER_STEPS = self.ownerComp.par.Slidersteps.eval()
		val = str(val)[:SLIDER_STEPS]
		inner = val.center(SLIDER_STEPS)
		return "[" + val + "]"
		
	def _buildComponent(self):
		fontSize   = self.ownerComp.par.fontsize.eval()
		numRows    = self.ownerComp.op('outputTable').numRows
		labelSize  = self.ownerComp.par.Maxchars.eval()
		sliderSize = self.ownerComp.par.Slidersteps.eval()
		totalCols  = labelSize + sliderSize + 2 
	
		charAspect    = 0.6
		rowPadding    = 1.2
	
		compWidth  = fontSize * charAspect * totalCols
		compHeight = fontSize * ((numRows) * rowPadding)
	
		self.ownerComp.par.w.val = compWidth
		self.ownerComp.par.h.val = compHeight
		
	# ── Public update API ───────────────────────────────────────────────────
	def GetParName(self, name):
		return self._parName(name)
	
	def UpdateSliderVal(self, parName, val):
		for item in self.LAYOUT:
			if item.get("type") == "slider" and self._parName(item) == parName:
				row     = self._getTableRow(item)
				inverse = item.get("inverse", False)
				if row is not None:
					self.outputTable[row, 1] = self._getSliderVal(val, inverse=inverse)
				return
				
	
	def PressButton(self, parName, val):
		self.buttonState[parName] = bool(val)
		for item in self.LAYOUT:
			if item.get("type") == "button" and self._parName(item) == parName:
				row = self._getTableRow(item)
				if row is not None:
					self.outputTable[row, 1] = self._getButtonVal(bool(val))
				return
	
	def SelectMenu(self, parName, index):
		if hasattr(self.ownerComp.par, parName):
			self.ownerComp.par[parName].val = index
	
		for item in self.LAYOUT:
			if item.get("type") == "radioButtons" and self._parName(item) == parName:
				options = item.get("options", [])
				index   = int(tdu.clamp(index, 0, len(options) - 1))
				for i in range(len(options)):
					row = self._getTableRow(item, i)
					if row is not None:
						self.outputTable[row, 1] = self._getMenuOptionVal(i == index)
				return
				
	def GetRowInfo(self, row):
		if row is None or row >= len(self.rowMap):
			return None
		item, optionIndex = self.rowMap[row]
		t       = item.get("type")
		name    = item.get("name", "")
		parName = self._parName(item) if t not in ("divider", "header") else None
		return (t, name, parName, optionIndex)
				
	def UpdateFromPanel(self, fromClick=False):
		info = self.GetRowInfo(self.SelectedRow)
		if info is None:
			return
	
		t, name, parName, optionIndex = info
	
		# Bail early if this element is marked non-interactable
		item = next((i for i in self.LAYOUT if i.get("name") == name), None)
		if item is None or not self._isInteractable(item):
			return
	
		if t == "slider" and self.Clicked:

			val = tdu.clamp(self.InsideU, 0.0, 1.0)
			if hasattr(self.ownerComp.par, parName):
				self.ownerComp.par[parName].val = val
			self.UpdateSliderVal(parName, val)
	
		elif t == "button" and fromClick:
			btnStyle = next(i for i in self.LAYOUT if i.get("name") == name).get("btnStyle", "Momentary")
			if btnStyle == "Toggle":
				if self.Clicked:
					newState = not self.buttonState.get(parName, False)
					self.PressButton(parName, newState)
					if hasattr(self.ownerComp.par, parName):
						self.ownerComp.par[parName].val = 1 if newState else 0
			else:
				self.PressButton(parName, self.Clicked)
				if hasattr(self.ownerComp.par, parName):
					self.ownerComp.par[parName].val = 1 if self.Clicked else 0
	
		elif t == "radioButtons" and self.Clicked:
			self.SelectMenu(parName, optionIndex)
			
	def UpdateThrobberVal(self, parName, val):
		for item in self.LAYOUT:
			if item.get("type") == "throbber" and self._parName(item) == parName:
				row = self._getTableRow(item)
				if row is not None:
					self.outputTable[row, 1] = self._getThrobberVal(val % 1)
				return
				
	def UpdateStringVal(self, parName, val):
		for item in self.LAYOUT:
			if item.get("type") == "stringDisplay" and self._parName(item) == parName:
				row = self._getTableRow(item)
				if row is not None:
					self.outputTable[row, 1] = self._getStringVal(str(val))
				return
				
	##---------MIDIMAPPING---------##
	def MidiMap(self, remove=False):
		if not self.ownerComp.par.Midimap: return
	
		info = self.GetRowInfo(self.SelectedRow)
		if info is None: return
		t, name, parName, optionIndex = info
	
		targetPar = f"{parName}dummy{optionIndex}" if (t == "radioButtons" and optionIndex is not None) else parName
	
		if remove:
			self.armedForMidi = None
			self.ownerComp.par[targetPar].bindExpr = ""
			return
	
		self.armedForMidi = targetPar

		
	def WhenMidiChanges(self, midiChan):
		if self.armedForMidi is None: return
		bindExp = f"op('./bind1')['{midiChan}']"
		

		self.ownerComp.par[self.armedForMidi].bindExpr = bindExp
		self.armedForMidi = None
		
		return
	
	###-----------ON INIT----------------------##

	def onInitTD(self):
		self.sliderChar  = self.ownerComp.par.Slidercharacter.eval()
		self.emptyChar   = self.ownerComp.par.Emptycharacter.eval()
		self.buttonState = {}
		self._buildParameters()
		self._buildTable()
		self.rowMap = self._buildRowMap()
		self._buildComponent()
		
		op('postSetUp').run()
