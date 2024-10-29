import csv
import sys
from datetime import datetime

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QColor, QTextCharFormat
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
                error_dialog = ErrorWindow("No stock available, data error")
                error_dialog.exec()

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
        self.quantitySpinBox.setRange(1, 1000)  # Set a reasonable range for quantity
        self.quantitySpinBox.setValue(1)  # Default value

        # TODO: create QLabels to show the Stock purchase total
        self.InitQlabels()

        # Create a QLabel for the information icon
        self.infoIconLabel = QLabel("i")  # Use "i" or any icon representation you prefer
        self.infoIconLabel.setStyleSheet("font-size: 14px;")  # Make "i" smaller
        self.infoIconLabel.setAlignment(Qt.AlignmentFlag.AlignRight)  # Align to the right

        # HTML for tooltip with color cubes
        self.infoIconLabel.setToolTip(
            "Calendar's Legend:<br>"
            "• <span style='color: purple;'>■</span> Indicates dates with stock data.<br>"
            "• <span style='color: gray;'>■</span> Indicates dates without stock data."
        )

        # TODO: create QLabels to show the Stock sell total
        # TODO: create QLabels to show the Stock profit total
        # TODO: initialize the layout - 6 rows to start

        # Create layout
        layout = QGridLayout()

        # Info icon 
        layout.addWidget(self.infoIconLabel, 0, 2)  

        layout.addWidget(self.stockLabel, 1, 0)
        layout.addWidget(self.stockComboBox, 1, 1)

        # Add the sell and buy calendar
        layout.addWidget(QLabel("Purchase Date:"), 2, 0)
        layout.addWidget(self.buyCalendar, 2, 1)  # Buy calendar below
        layout.addWidget(QLabel("Sell Date:"), 3, 0)
        layout.addWidget(self.sellCalendar, 3, 1)  # Sell calendar below

        layout.addWidget(QLabel("Quantity:"), 4, 0)
        layout.addWidget(self.quantitySpinBox, 4, 1)
        layout.addWidget(self.purchaseTotalLabel, 5, 0, 1, 2)
        layout.addWidget(self.sellTotalLabel, 6, 0, 1, 2)
        layout.addWidget(self.profitTotalLabel, 7, 0, 1, 2)

        self.setLayout(layout)

        # TODO: set the calendar values
        # purchase: two weeks before most recent
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
                error_dialog = ErrorWindow(
                    f"Selected buy date is after sell date, impossible calcul"
                )
                error_dialog.exec()
                # Reset the labels
                self.InitQlabels()
                return

            # TODO: perform necessary calculations to calculate totals
            # Convert QDates to tuples for dictionary lookup
            buy_date_tuple = (buy_date.year(), buy_date.month(), buy_date.day())
            sell_date_tuple = (sell_date.year(), sell_date.month(), sell_date.day())

            # Check if stock is in data
            if selected_stock not in self.data:
                error_dialog = ErrorWindow(
                    f"Stock '{selected_stock}' is not available in the dataset."
                )
                error_dialog.exec()
                # Reset the labels
                self.InitQlabels()
                return

            # Check if the selected dates are in the data for this stock
            buy_price = self.data[selected_stock].get(buy_date_tuple, None)
            sell_price = self.data[selected_stock].get(sell_date_tuple, None)

            if buy_price is None:
                error_dialog = ErrorWindow(
                    "The selected purchase date does not match our available data."
                )
                error_dialog.exec()
                # Reset the labels
                self.InitQlabels()
                return
            if sell_price is None:
                error_dialog = ErrorWindow(
                    "The selected sell date does not match our available data."
                )
                error_dialog.exec()
                # Reset the labels
                self.InitQlabels()
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
        
    def InitQlabels(self):
        self.purchaseTotalLabel = QLabel("Purchase Total: $0.00", self)
        self.sellTotalLabel = QLabel("Sell Total: $0.00", self)
        self.profitTotalLabel = QLabel("Profit: $0.00", self)

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
        available_format.setBackground(darker_selection_color)  # Darker selection color for available dates

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


# Creating a class called ErrorWindow to show the problem to the user in case of a problem
# like not having data of a stock at all or on a certain time
class ErrorWindow(QDialog):
    def __init__(self, message):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Error")

        # Create a label with the error message
        self.errorLabel = QLabel(message, self)

        # Create an "OK" button to close the dialog
        self.okButton = QPushButton("OK", self)
        self.okButton.clicked.connect(self.accept)

        # Arrange the label and button vertically
        layout = QVBoxLayout()
        layout.addWidget(self.errorLabel)
        layout.addWidget(self.okButton)
        self.setLayout(layout)


# This is complete
if __name__ == "__main__":
    app = QApplication(sys.argv)
    stock_calculator = StockTradeProfitCalculator()
    stock_calculator.show()
    sys.exit(app.exec())
