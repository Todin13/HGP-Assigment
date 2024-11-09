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
                self,
                "Error",
                f"Themes {theme} does not exist going back to system theme.",
            )
            palette = QApplication.palette()

        # Apply the palette to the main window
        self.setPalette(palette)

        # Update colors for menu and tooltips based on the selected theme
        highlight_color = palette.color(QPalette.ColorRole.Highlight).name()
        darker_bg_color = palette.color(QPalette.ColorRole.Window).darker(150).name()
        window_text_color = palette.color(QPalette.ColorRole.WindowText).name()
        background_color = palette.color(QPalette.ColorRole.Window).name()
        alternate_bg_color = palette.color(QPalette.ColorRole.AlternateBase).name()

        # Updating the menu_style
        menu_style = f"""
            QMenuBar {{ 
                background-color: {darker_bg_color}; 
                color: {window_text_color};
            }}
            QMenuBar::item {{ 
                background-color: transparent; 
            }}
            QMenuBar::item:selected {{ 
                background-color: {highlight_color}; 
                color: {window_text_color};
            }}
            QMenu {{ 
                background-color: {background_color}; 
                color: {window_text_color};
            }}
            QMenu::item {{ 
                background-color: transparent;
            }}
            QMenu::item:selected {{ 
                background-color: {highlight_color}; 
                color: {window_text_color};
            }}
        """
        self.menuBar().setStyleSheet(menu_style)

        # Update dock widget 
        dock_style = dock_style = f"""
            QDockWidget {{
                background-color: {background_color};
                color: {window_text_color};
                border: 1px solid {highlight_color};
            }}
            QDockWidget::title {{
                background-color: {darker_bg_color};
                color: {window_text_color};
                padding: Opx;
                font-weight: bold;
            }}
            QDockWidget::close-button, QDockWidget::float-button {{
                background-color: {highlight_color};
                border-radius: 3px;
            }}
            QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
                background-color: {alternate_bg_color};
            }}
            QLabel, QTextEdit, QListView {{
                color: {window_text_color};
            }}
        """

        self.dockInfo.setStyleSheet(dock_style)
        self.playerInfo.setStyleSheet(dock_style)
        self.playerInfo.setAutoFillBackground(True)

        # Update
        self.update() 