from PySide6.QtWidgets import QStyledItemDelegate, QApplication, QStyle, QStyleOptionViewItem, QStyleOptionButton
from PySide6.QtCore import Qt, QEvent, QRect
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor

class CheckDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, fill="#1fbe8b", tick="#111827"):
        super().__init__(parent)
        self.fill = QColor(fill)
        self.tick = QColor(tick)

    def paint(self, painter, option, index):
        state = index.data(Qt.CheckStateRole)
        r = option.rect
        size = min(r.height(), 18)
        box = QRect(r.x() + (r.width()-size)//2, r.y() + (r.height()-size)//2, size, size)

        painter.save()
        try:
            painter.setRenderHint(QPainter.Antialiasing, True)

            # caja
            if state == Qt.Checked:
                painter.setBrush(self.fill)
                painter.setPen(Qt.NoPen)
            else:
                painter.setBrush(QColor("#2a2a2a"))
                painter.setPen(QPen(QColor("#3a3a3a")))
            painter.drawRoundedRect(box, 4, 4)

            # chulo
            if state == Qt.Checked:
                pen = QPen(self.tick)
                pen.setWidthF(2.2)              # mejor que pasar 2.2 en el ctor
                pen.setCapStyle(Qt.RoundCap)
                pen.setJoinStyle(Qt.RoundJoin)
                painter.setPen(pen)
                painter.setBrush(Qt.NoBrush)    # por si acaso, que no intente rellenar

                x, y, w, h = box.x(), box.y(), box.width(), box.height()
                path = QPainterPath()
                path.moveTo(x + 0.25*w, y + 0.55*h)
                path.lineTo(x + 0.45*w, y + 0.75*h)
                path.lineTo(x + 0.75*w, y + 0.30*h)
                painter.drawPath(path)
        except Exception as e:
            print("Delegate paint error:", e)
        finally:
            painter.restore()   # SIEMPRE se ejecuta

    # Toggle con click
    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease and option.rect.contains(event.pos()):
            cur = index.data(Qt.CheckStateRole)
            model.setData(index, Qt.Unchecked if cur == Qt.Checked else Qt.Checked, Qt.CheckStateRole)
            return True
        return False