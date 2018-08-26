import pymel.core as pm


def getFCurveValues(fcv_node, division, factor=1):
    incr = 1 / (division - 1.0)

    values = []
    for i in range(division):
        pm.setAttr(fcv_node + ".input", i * incr)
        values.append(pm.getAttr(fcv_node + ".output") * factor)

    return values
