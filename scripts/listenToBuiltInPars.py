

from typing import Any, List
pComp = parent.tinyUI
def onValueChange(par: Par, prev: Any):
	if par.name == "Fontsize":
		pComp.UpdateComponent()
	return

