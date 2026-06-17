from typing import Any, List
pComp = parent.tinyUI
def onValueChange(par: Par, prev: Any):


	if par.style == "Float":
		is_throbber = any(
			item.get("type") == "throbber" and pComp.GetParName(item["name"]) == par.name
			for item in pComp.LAYOUT
		)
		if is_throbber:
			pComp.UpdateThrobberVal(par.name, par.eval())
		else:
			pComp.UpdateSliderVal(par.name, par.eval())

	elif par.style == "Str":
		pComp.UpdateStringVal(par.name, par.eval())

	elif par.style == "Int":
		pComp.SelectMenu(par.name, par.eval())

	elif par.style in ("Momentary", "Toggle"):
		if "dummy" in par.name and par.eval():
			baseName, _, index = par.name.rpartition("dummy")
			if index.isdigit():
				is_dummy = any(
					item.get("type") == "radioButtons" and pComp.GetParName(item["name"]) == baseName
					for item in pComp.LAYOUT
				)
				if is_dummy:
					pComp.SelectMenu(baseName, int(index))
					return
		pComp.PressButton(par.name, par.eval())
