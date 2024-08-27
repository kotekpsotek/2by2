from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex

class MyTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def insertRows(self, position, rows, data, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
    
        for i in range(rows):
            self._data.append(data)
            
        self.endInsertRows()
    
        return True

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]

    def flags(self, index):
        return Qt.ItemIsEnabled  # Make all items non-editable
