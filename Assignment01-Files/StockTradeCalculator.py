import csv
import sys
from datetime import datetime

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QColor, QTextCharFormat, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QComboBox,
    QDialog,
    QGridLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QFrame,
    QMenu,
    QHBoxLayout,
    QMessageBox,
)


class StockTradeProfitCalculator(QDialog):
    """
    Provides the following functionality:

    - Allows the selection of the stock to be purchased
    - Allows the selection of the quantity to be purchased
    - Allows the selection of the purchase date
    - Displays the purchase total
    - Allows the selection of the sell date
    - Displays the sell total
    - Displays the profit total
    """

    def __init__(self):
        """
        This method requires substantial updates.
        Each of the widgets should be suitably initialized and laid out.
        """
        super().__init__()

        # setting up dictionary of Stocks
        self.data = self.make_data()

        # Check if 'Amazon' exists, if not, handle it gracefully
        if "Amazon" in self.data:
            defaultDate = sorted(self.data["Amazon"].keys())[-1]

            # transforming tuple to qdate if it exist
            self.sellCalendarDefaultDate = QDate(
                defaultDate[0], defaultDate[1], defaultDate[2]
            )
        else:
            print(
                "Amazon not found in the dataset. Available stocks:", self.data.keys()
            )
            self.sellCalendarDefaultDate = (
                QDate.currentDate()
            )  # Default to the current date
            # Adding error message to tell the user if there is no stock available
            if not self.data.keys():
                QMessageBox.critical(
                    self, "Error", "No stock available, data error"
                )

        # TODO: Define buyCalendarDefaultDate
        self.buyCalendarDefaultDate = (
            self.sellCalendarDefaultDate
        )  # setting to be the same as selldefaultDate to not have problem.

        # TODO: create QLabel for Stock selection
        self.stockLabel = QLabel("Select Stock:", self)

        # TODO: create QComboBox and populate it with a list of Stocks
        self.stockComboBox = QComboBox(self)
        self.stockComboBox.addItems(self.data.keys())

        # TODO: create CalendarWidgets for selection of purchase and sell dates
        self.buyCalendar = QCalendarWidget(self)
        self.sellCalendar = QCalendarWidget(self)

        # Set default dates for calendars
        self.buyCalendar.setSelectedDate(self.buyCalendarDefaultDate)
        self.sellCalendar.setSelectedDate(self.sellCalendarDefaultDate)

        # TODO: create QSpinBox to select Stock quantity purchased
        self.quantitySpinBox = QSpinBox(self)
        self.quantitySpinBox.setRange(1, 100000)
        self.quantitySpinBox.setValue(1)  # Default value

        # TODO: create QLabels to show the Stock purchase total
        self.purchaseTotalLabel = QLabel("Purchase Total: $0.00", self)
        self.sellTotalLabel = QLabel("Sell Total: $0.00", self)
        self.profitTotalLabel = QLabel("Profit: $0.00", self)

        #  Create a QFrame to hold the top bar
        self.infoFrame = QFrame()
        self.infoFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.infoFrame.setStyleSheet(f"background-color: {'grey'}")  # Init of the color to grey because not to strong for the eyes and can be good both in light and dark mode

        # Theme changer
        self.themeChanger = QPushButton("Themes", self)
        self.themeChanger.setMenu(self.change_theme())
        self.themeChanger.setFixedSize(90, 20)
        self.themeChanger.setStyleSheet("font-size: 15px; padding: 0px; margin: 0px;")

        # Create a QLabel for the information icon
        self.infoIconLabel = QPushButton("info", self)
        self.infoIconLabel.setFixedSize(90, 20)
        self.infoIconLabel.setStyleSheet("font-size: 15px; padding: 0px; margin: 0px;")

        # Init/Default info text shown on click on infoInconLabel 
        self.info_text = (
            "Calendar's Legend:<br>"
            f"• <span style='color: {'blue'};'>■</span> Indicates dates with stock data.<br>"
            f"• <span style='color: {'#A9A9A9'};'>■</span> Indicates dates without stock data."
        )

        # Connect the info button's clicked signal to a method
        self.infoIconLabel.clicked.connect(self.show_info)

        # Add the info icon label to the frame
        topLayout = QHBoxLayout(self.infoFrame)
        topLayout.addWidget(self.themeChanger)
        topLayout.addWidget(self.infoIconLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.setSpacing(0)

        mainLayout = QVBoxLayout()

        # Set the content margin of the main layout
        mainLayout.setContentsMargins(0, 0, 0, 0)

        # Add the frame to the main layout
        mainLayout.addWidget(self.infoFrame)

        # TODO: create QLabels to show the Stock sell total
        # TODO: create QLabels to show the Stock profit total
        # TODO: initialize the layout - 6 rows to start

        # Create the body layout
        bodyLayout = QGridLayout()

        # Set the content margin of the body layout
        bodyLayout.setContentsMargins(10, 10, 10, 10)

        # Adding the stock choosing box
        bodyLayout.addWidget(self.stockLabel, 1, 0)
        bodyLayout.addWidget(self.stockComboBox, 1, 1)

        # Add the sell and buy calendar
        bodyLayout.addWidget(QLabel("Purchase Date:"), 2, 0)
        bodyLayout.addWidget(self.buyCalendar, 2, 1)  # Buy calendar below
        bodyLayout.addWidget(QLabel("Sell Date:"), 3, 0)
        bodyLayout.addWidget(self.sellCalendar, 3, 1)  # Sell calendar below

        bodyLayout.addWidget(QLabel("Quantity:"), 4, 0)
        bodyLayout.addWidget(self.quantitySpinBox, 4, 1)
        bodyLayout.addWidget(self.purchaseTotalLabel, 5, 0, 1, 2)
        bodyLayout.addWidget(self.sellTotalLabel, 6, 0, 1, 2)
        bodyLayout.addWidget(self.profitTotalLabel, 7, 0, 1, 2)

        mainLayout.addLayout(bodyLayout)

        self.setLayout(mainLayout)

        # apply default theme (system theme)
        self.apply_theme("System")

        # TODO: set the calendar values
        # purchase: most recent
        self.buyCalendar.setSelectedDate(self.buyCalendarDefaultDate)
        # sell: most recent
        self.sellCalendar.setSelectedDate(self.sellCalendarDefaultDate)

        # TODO: connecting signals to slots so that a change in one control updates the UI
        self.stockComboBox.currentIndexChanged.connect(self.updateUi)
        self.buyCalendar.selectionChanged.connect(self.updateUi)
        self.sellCalendar.selectionChanged.connect(self.updateUi)
        self.quantitySpinBox.valueChanged.connect(self.updateUi)

        # TODO: set the window title
        self.setWindowTitle("Stock Trade Profit Calculator")
        # TODO: update the UI
        self.updateUi()

    def updateUi(self):
        """
        This requires substantial development.
        Updates the UI when control values are changed; should also be called when the app initializes.
        """
        try:

            # update the calendar to show the AvailableDate in different color
            self.highlightAvailableDates()

            # TODO: get selected dates, stocks and quantity
            selected_stock = self.stockComboBox.currentText()
            buy_date = self.buyCalendar.selectedDate()
            sell_date = self.sellCalendar.selectedDate()
            quantity = self.quantitySpinBox.value()

            # Check if buy is before sell
            if buy_date > sell_date:
                QMessageBox.critical(
                    self, "Error", f"Selected buy date is after sell date, impossible calcul"
                )
                # Reset the labels
                self.ResetCalculusLabels()
                return

            # TODO: perform necessary calculations to calculate totals
            # Convert QDates to tuples for dictionary lookup
            buy_date_tuple = (buy_date.year(), buy_date.month(), buy_date.day())
            sell_date_tuple = (sell_date.year(), sell_date.month(), sell_date.day())

            # Check if stock is in data
            if selected_stock not in self.data:
                
                QMessageBox.critical(
                    self, "Error", f"Stock '{selected_stock}' is not available in the dataset."
                )
                # Reset the labels
                self.ResetCalculusLabels()
                return

            # Check if the selected dates are in the data for this stock
            buy_price = self.data[selected_stock].get(buy_date_tuple, None)
            sell_price = self.data[selected_stock].get(sell_date_tuple, None)

            if buy_price is None:
                QMessageBox.critical(
                    self, "Error", "The selected purchase date does not match our available data."
                )
                # Reset the labels
                self.ResetCalculusLabels()
                return
            if sell_price is None:
                QMessageBox.critical(
                    self, "Error", "The selected sell date does not match our available data."
                )
                # Reset the labels
                self.ResetCalculusLabels()
                return

            # Calculate totals
            purchase_total = buy_price * quantity
            sell_total = sell_price * quantity
            profit = sell_total - purchase_total

            # TODO: update the label displaying totals
            # Update the labels with calculated values
            self.purchaseTotalLabel.setText(f"Purchase Total: ${purchase_total:.2f}")
            self.sellTotalLabel.setText(f"Sell Total: ${sell_total:.2f}")
            self.profitTotalLabel.setText(f"Profit: ${profit:.2f}")

        except Exception as e:
            print(f"Error in updateUi: {e}")

    def make_data(self):
        """
        This code reads the stock market CSV file and generates a dictionary structure.
        :return: a dictionary of dictionaries
        """
        data = {}
        try:
            with open("Transformed_Stock_Market_Dataset.csv", mode="r") as file:
                reader = csv.DictReader(file)
                stock_names = reader.fieldnames[
                    1:
                ]  # All columns except 'Date' are stock names

                for row in reader:
                    date_string = row["Date"]
                    date_tuple = self.string_date_into_tuple(date_string)

                    for stock in stock_names:
                        price = row[stock].replace(",", "")
                        try:
                            price = float(price)
                        except ValueError:
                            price = 0.0

                        if stock not in data:
                            data[stock] = {}

                        data[stock][date_tuple] = price

            print("Data loaded successfully.")
            print(
                f"Stocks available: {stock_names}"
            )  # Debugging: Print all available stock names

        except Exception as e:
            print(f"Error reading data: {e}")
        return data

    def string_date_into_tuple(self, date_string):
        """
        Converts a date in string format (e.g., "2024-02-02") into a tuple (year, month, day).
        :return: tuple representing the date
        """
        try:
            if "-" in date_string:
                date_obj = datetime.strptime(date_string, "%d-%m-%Y")
            else:
                date_obj = datetime.strptime(date_string, "%m/%d/%Y")
            return date_obj.year, date_obj.month, date_obj.day
        except ValueError:
            print(f"Error parsing date: {date_string}")
            return None

    def ResetCalculusLabels(self):
        self.purchaseTotalLabel.setText("Purchase Total: $0.00")
        self.sellTotalLabel.setText("Sell Total: $0.00")
        self.profitTotalLabel.setText("Profit: $0.00")

    def highlightAvailableDates(self):
        """
        Highlights dates in the buy and sell calendars where data for the selected stock is available.
        Adds tooltips with stock prices and dims unavailable dates. Disables dates outside the range of available data.
        """
        # Clear previous highlights and tooltips
        self.buyCalendar.setDateTextFormat(QDate(), QTextCharFormat())
        self.sellCalendar.setDateTextFormat(QDate(), QTextCharFormat())

        # Get selected stock
        selected_stock = self.stockComboBox.currentText()
        if selected_stock not in self.data:
            return

        # Get the application's selection color and make it darker
        selection_color = self.palette().color(self.palette().ColorRole.Highlight)
        darker_selection_color = selection_color.darker(150)  # Adjust darkness level

        # Define formats using the darker selection color
        available_format = QTextCharFormat()
        available_format.setBackground(
            darker_selection_color
        )  # Darker selection color for available dates

        unavailable_format = QTextCharFormat()
        unavailable_format.setForeground(
            QColor("#A9A9A9")
        )  # Gray for unavailable dates

        # Get all available dates for the selected stock
        stock_dates = self.data[selected_stock].keys()
        min_date_tuple = min(stock_dates)
        max_date_tuple = max(stock_dates)
        min_date = QDate(*min_date_tuple)
        max_date = QDate(*max_date_tuple)

        # Set calendar date range to disable dates outside of available data
        self.buyCalendar.setMinimumDate(min_date)
        self.buyCalendar.setMaximumDate(max_date)
        self.sellCalendar.setMinimumDate(min_date)
        self.sellCalendar.setMaximumDate(max_date)

        # Apply highlighting for available dates and dimming for unavailable dates
        for date in self.iterate_dates(min_date, max_date):
            date_tuple = (date.year(), date.month(), date.day())
            if date_tuple in stock_dates:
                # Highlight available dates and set tooltip with stock price
                self.buyCalendar.setDateTextFormat(date, available_format)
                self.sellCalendar.setDateTextFormat(date, available_format)
                price = self.data[selected_stock][date_tuple]
                self.buyCalendar.setToolTip(f"{date.toString()} - Price: ${price:.2f}")
                self.sellCalendar.setToolTip(f"{date.toString()} - Price: ${price:.2f}")
            else:
                # Dim unavailable dates within the range
                self.buyCalendar.setDateTextFormat(date, unavailable_format)
                self.sellCalendar.setDateTextFormat(date, unavailable_format)

    def iterate_dates(self, start_date, end_date):
        """
        Yields each date from start_date to end_date.
        """
        current_date = start_date
        while current_date <= end_date:
            yield current_date
            current_date = current_date.addDays(1)

    def change_theme(self):
        menu = QMenu(self)

        # Create actions for each theme with proper connections
        action_system = menu.addAction("System")
        action_system.triggered.connect(lambda: self.apply_theme("System"))

        action_light = menu.addAction("Light")
        action_light.triggered.connect(lambda: self.apply_theme("Light"))

        action_dark = menu.addAction("Dark")
        action_dark.triggered.connect(lambda: self.apply_theme("Dark"))

        action_dark_blue = menu.addAction("Dark Blue")
        action_dark_blue.triggered.connect(lambda: self.apply_theme("Dark Blue"))

        return menu

    def apply_theme(self, theme):
        palette = QPalette()

        # Define colors for themes
        if theme == "System":
            # Reset to system's default palette
            palette = QApplication.palette()
        elif theme == "Light":
            palette.setColor(QPalette.ColorRole.Window, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#F0F0F0"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#3399FF"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
        elif theme == "Dark":
            palette.setColor(QPalette.ColorRole.Window, QColor("#2E2E2E"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#3E3E3E"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#2E2E2E"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#2E2E2E"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#3E3E3E"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#505050"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
        elif theme == "Dark Blue":
            palette.setColor(QPalette.ColorRole.Window, QColor("#282A36"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#F8F8F2"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#44475A"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#282A36"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#282A36"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#F8F8F2"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#F8F8F2"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#44475A"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#F8F8F2"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#6272A4"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#F8F8F2"))
        else:
            QMessageBox.critical(
                    self, "Error", f"Themes {theme} does not exist going back to system theme."
            )
            palette = QApplication.palette()

        # Apply the palette to the main window
        self.setPalette(palette)

        # Update the color type
        selection_color = self.palette().color(self.palette().ColorRole.Highlight)
        stock_data_color = selection_color.darker(150).name()
        no_data_color = "#A9A9A9"
        info_frame_color = selection_color.name()


        # Updating the menu_style
        menu_style = f"""
                    QMenu {{ background-color: {info_frame_color}; color: {no_data_color}; }}
                    QMenu::item {{ background-color: transparent; }}
                    QMenu::item:selected {{ background-color: {stock_data_color}; color: {no_data_color}; }}
                """

        # Update the menu style using setStyleSheet
        self.themeChanger.setStyleSheet(menu_style)

        # Update the tooltip with color cubes based on the selected theme
        self.info_text = (
            f"Calendar's Legend:<br>"
            f"• <span style='color: {stock_data_color};'>■</span> Indicates dates with stock data.<br>"
            f"• <span style='color: {no_data_color};'>■</span> Indicates dates without stock data."
        )

        # Update the info frame background color
        self.infoFrame.setStyleSheet(f"background-color: {info_frame_color};")

    
    # Method to display information
    def show_info(self):
        QMessageBox.information(self, "Info", self.info_text)

# This is complete
if __name__ == "__main__":
    app = QApplication(sys.argv)
    stock_calculator = StockTradeProfitCalculator()
    stock_calculator.show()
    sys.exit(app.exec())
