from PySide6.QtWidgets import QStyledItemDelegate, QApplication, QStyle, QStyleOptionViewItem, QStyleOptionButton
from PySide6.QtCore import Qt, QEvent, QRect

class CheckDelegate(QStyledItemDelegate):
    def paint(self, painter, option: QStyleOptionViewItem, index):
        # Dibuja el fondo y el foco normal del item
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        opt.text = ""  # sin texto en la col de check
        style = opt.widget.style() if opt.widget else QApplication.style()
        style.drawControl(QStyle.CE_ItemViewItem, opt, painter, opt.widget)

        # Dibuja el checkbox centrado según CheckStateRole
        chk_opt = QStyleOptionButton()
        chk_opt.state = QStyle.State_Enabled
        if index.data(Qt.CheckStateRole) == Qt.Checked:
            chk_opt.state |= QStyle.State_On
        else:
            chk_opt.state |= QStyle.State_Off

        ind_rect = style.subElementRect(QStyle.SE_CheckBoxIndicator, chk_opt, None)
        chk_opt.rect = QRect(
            option.rect.x() + (option.rect.width() - ind_rect.width()) // 2,
            option.rect.y() + (option.rect.height() - ind_rect.height()) // 2,
            ind_rect.width(), ind_rect.height()
        )
        style.drawControl(QStyle.CE_CheckBox, chk_opt, painter)

    def editorEvent(self, event, model, option, index):
        # Toggle con click izquierdo en cualquier parte de la celda
        if event.type() in (QEvent.MouseButtonRelease, QEvent.MouseButtonDblClick):
            if event.button() == Qt.LeftButton:
                cur = index.data(Qt.CheckStateRole)
                model.setData(index, Qt.Unchecked if cur == Qt.Checked else Qt.Checked, Qt.CheckStateRole)
                return True
        return False
