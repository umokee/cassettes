from PySide6.QtWidgets import QComboBox, QStyledItemDelegate
from PySide6.QtGui import QStandardItem, QPalette, QFontMetrics
from PySide6.QtCore import Qt, QEvent
from typing import Any


class MultiSelectComboBox(QComboBox):
    """
    A custom combo box widget that allows for multi-select functionality.

    This widget provides the ability to select multiple items from a dropdown list and display them in a comma-separated format in the combo box's line edit area.
    """

    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.placeholderText = ""

        self.setEditable(True)
        self.lineEdit().setReadOnly(True)

        palette = self.lineEdit().palette()
        palette.setBrush(
            QPalette.ColorRole.Base, palette.brush(QPalette.ColorRole.Button)
        )
        self.lineEdit().setPalette(palette)

        self.setItemDelegate(MultiSelectComboBox.Delegate())
        self.setOutputType("data")
        self.setDisplayType("text")
        self.setDisplayDelimiter(",")

        self.model().dataChanged.connect(self.updateText)
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False
        self.view().viewport().installEventFilter(self)

    def setOutputType(self, output_type: str) -> None:
        """Set the output type for the combo box.

        Args:
            output_type (str): The output type, either 'data' or 'text'.

        Raises:
            ValueError: If output_type is neither 'data' nor 'text'.
        """
        if output_type in ["data", "text"]:
            self.output_type = output_type
        else:
            raise ValueError("Output type must be 'data' or 'text'")

    def setDisplayType(self, display_type: str) -> None:
        """Set the display type for the combo box.

        Args:
            display_type (str): The display type, either 'data' or 'text'.

        Raises:
            ValueError: If display_type is neither 'data' nor 'text'.
        """
        if display_type in ["data", "text"]:
            self.display_type = display_type
        else:
            raise ValueError("Display type must be 'data' or 'text'")

    def getOutputType(self) -> str:
        """Get the current output type.

        Returns:
            str: The current output type, either 'data' or 'text'.
        """
        return self.output_type

    def getDisplayType(self) -> str:
        """Get the current display type.

        Returns:
            str: The current display type, either 'data' or 'text'.
        """
        return self.display_type

    def setDisplayDelimiter(self, delimiter: str, space_after: bool = True, space_before: bool = False) -> None:
        """Set the display delimiter for the combo box.

        Args:
            delimiter (str): The delimiter to use.
            space_after (bool): Whether to add a space after the delimiter. Default is True.
            space_before (bool): Whether to add a space before the delimiter. Default is False.
        """
        sufix = " " if space_after else ""
        prefix = " " if space_before else ""
        self.display_delimiter = prefix + delimiter + sufix

    def getDisplayDelimiter(self) -> str:
        """Get the current display delimiter.

        Returns:
            str: The current display delimiter.
        """
        return self.display_delimiter

    def resizeEvent(self, event) -> None:
        """Resize event handler.

        Args:
            event: The resize event.
        """
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, obj, event) -> bool:
        """Event filter to handle mouse button release events.

        Args:
            obj: The object emitting the event.
            event: The event being emitted.

        Returns:
            bool: True if the event was handled, False otherwise.
        """
        if obj == self.lineEdit() and event.type() == QEvent.Type.MouseButtonRelease:
            if self.closeOnLineEditClick:
                self.hidePopup()
            else:
                self.showPopup()
            return True
        if obj == self.view().viewport() and event.type() == QEvent.Type.MouseButtonRelease:
            index = self.view().indexAt(event.position().toPoint())
            item = self.model().itemFromIndex(index)
            if item.checkState() == Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Unchecked)
            else:
                item.setCheckState(Qt.CheckState.Checked)
            return True
        return False

    def showPopup(self) -> None:
        """Show the combo box popup.
        """
        super().showPopup()
        self.closeOnLineEditClick = True

    def hidePopup(self) -> None:
        """Hide the combo box popup.
        """
        super().hidePopup()
        self.startTimer(100)

    def timerEvent(self, event) -> None:
        """Timer event handler.

        Args:
            event: The timer event.
        """
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def typeSelection(self, index: int, type_variable: str, expected_type: str = "data") -> str:
        """Get the selected item's data or text based on type.

        Args:
            index (int): The index of the item.
            type_variable (str): The type variable to retrieve ('data' or 'text').
            expected_type (str): The expected type. Default is 'data'.

        Returns:
            str: The selected item's data or text.
        """
        if type_variable == expected_type:
            return self.model().item(index).data()
        return self.model().item(index).text()

    def updateText(self) -> None:
        """Update the displayed text based on selected items.
        """
        display_type = self.getDisplayType()
        delimiter = self.getDisplayDelimiter()
        texts = [self.typeSelection(i, display_type) for i in range(self.model(
        ).rowCount()) if self.model().item(i).checkState() == Qt.CheckState.Checked]
        
        if texts:
            text = delimiter.join(texts)
        else:
            text = self.placeholderText if hasattr(self, 'placeholderText') else ""
        
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(
            text, Qt.TextElideMode.ElideRight, self.lineEdit().width()
        )
        self.lineEdit().setText(elidedText)

    def addItem(self, text: str, data: Any) -> None:
        """Add an item to the combo box.

        Args:
            text (str): The text to display.
            data (str): The associated data. Default is None.
        """
        item = QStandardItem()
        item.setText(text)
        item.setData(data or text)
        item.setFlags(
            Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable
        )
        item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts: list, dataList: list = None) -> None:
        """Add multiple items to the combo box.

        Args:
            texts (list): A list of texts to display.
            dataList (list): A list of associated data. Default is None.
        """
        dataList = dataList or [None] * len(texts)
        for text, data in zip(texts, dataList):
            self.addItem(text, data)

    def currentData(self) -> list:
        """Get the currently selected data.

        Returns:
            list: A list of currently selected data.
        """
        output_type = self.getOutputType()
        return [self.typeSelection(i, output_type) for i in range(self.model().rowCount()) if self.model().item(i).checkState() == Qt.CheckState.Checked]

    def setCurrentIndexes(self, indexes: list) -> None:
        """Set the selected items based on the provided indexes.

        Args:
            indexes (list): A list of indexes to select.
        """
        for i in range(self.model().rowCount()):
            self.model().item(i).setCheckState(
                Qt.CheckState.Checked if i in indexes else Qt.CheckState.Unchecked
            )
        self.updateText()

    def getCurrentIndexes(self) -> list:
        """Get the indexes of the currently selected items.

        Returns:
            list: A list of indexes of selected items.
        """
        return [i for i in range(self.model().rowCount()) if self.model().item(i).checkState() == Qt.CheckState.Checked]

    def setPlaceholderText(self, text: str) -> None:
        """Set the placeholder text for the combo box.

        Args:
            text (str): The placeholder text.
        """
        self.placeholderText = text
        self.updateText()

    def showEvent(self, event) -> None:
        """Show event handler.

        Args:
            event: The show event.
        """
        super().showEvent(event)
        self.updateText()
    
    def getCurrentOptions(self):
        """Get the currently selected options along with their associated data.

        Returns:
            list: A list of tuples containing the text and data of the currently selected options.
                Each tuple consists of (text, data).
        """
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.CheckState.Checked:
                res.append((self.model().item(i).text(),
                            self.model().item(i).data()))
        return res
    
    def getPlaceholderText(self):
        """Get the placeholder text currently set for the combo box.

        Returns:
            str: The placeholder text.
        """
        return self.placeholderText
    
    def setDuplicatesEnabled(self, enabled: bool) -> None:
        """Set whether duplicates are allowed in the combo box.

        Args:
            enabled (bool): Whether duplicates are allowed.
        """
        self.duplicatesEnabled = enabled

    def isDuplicatesEnabled(self) -> bool:
        """Check if duplicates are allowed in the combo box.

        Returns:
            bool: True if duplicates are allowed, False otherwise.
        """
        return self.duplicatesEnabled
    
    def setCheckedIds(self, ids: list[int]) -> None:
        """Отметить пункты, id которых в переданном списке."""
        for i in range(self.model().rowCount()):
            checked = self.model().item(i).data() in ids
            self.model().item(i).setCheckState(
                Qt.Checked if checked else Qt.Unchecked
            )
        self.updateText()
