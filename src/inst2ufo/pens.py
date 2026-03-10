from fontTools.pens.filterPen import ContourFilterPointPen


class RotateStartPointPen(ContourFilterPointPen):
    def filterContour(self, contour):
        contour.reverse()
        # off = contour.pop()
        # contour.insert(0, off)
        return contour
