

from typing import Any

pComp = parent.tinyUI

def onOffToOn(panelValue):
	if panelValue.name == "select":
		pComp.Clicked     = True
		pComp.SelectedRow = pComp.HoverRow
		pComp.UpdateFromPanel(fromClick=True)  

		pComp.MidiMap(False)
	elif panelValue.name == "rselect":
		pComp.SelectedRow = pComp.HoverRow
		pComp.MidiMap(True)
		

def onOnToOff(panelValue):
	if panelValue.name == "select":
		pComp.Clicked = False
		pComp.UpdateFromPanel(fromClick=True)  

def onValueChange(panelValue, prev):
	if panelValue.name == "insidev":
		
		numRows = pComp.op('outputTable').numRows
		v       = 1.0 - panelValue.val
		pComp.HoverRow = int(tdu.clamp(math.floor(v * numRows), 0, numRows - 1))
	
	elif panelValue.name == "u":
		u = panelValue.val
		sliderSteps = pComp.par.Slidersteps.eval()
		maxChars    = pComp.par.Maxchars.eval()
		totalWidth  = maxChars + sliderSteps + 2
		sliderStart = (maxChars + 1) / totalWidth   # the "|" is at maxChars+1
		sliderWidth = sliderSteps / totalWidth
	
		pComp.InsideU = tdu.clamp((u - sliderStart) / sliderWidth, 0.0, 1.0)
		pComp.UpdateFromPanel(fromClick=False)


		

