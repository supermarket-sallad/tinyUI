
pComp = parent.tinyUI
def onHoverStartGetAccept(comp, info):
	return False

def onDragStartGetItems(comp, info):
	if not pComp.par.Draggablepars:
		return []
	dragItems = pComp.GetSelectedPar()
	return [dragItems]


	
