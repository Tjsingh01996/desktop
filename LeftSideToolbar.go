package main

import (
	"context"
	"log"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

func SideToolBar() *widget.Toolbar {
	toolbar := widget.NewToolbar(
		widget.NewToolbarAction(theme.DocumentCreateIcon(), func() {
			log.Println("New document")
		}),
		widget.NewToolbarSeparator(),
		widget.NewToolbarAction(theme.ContentCutIcon(), func() {}),
		widget.NewToolbarAction(theme.ContentCopyIcon(), func() {}),
		widget.NewToolbarAction(theme.ContentPasteIcon(), func() {}),
		widget.NewToolbarSpacer(),
		widget.NewToolbarAction(theme.HelpIcon(), func() {
			log.Println("Display help")
		}),
	)
	// container.NewBorder(toolbar, nil, nil, nil, widget.NewLabel("Content"))

	return toolbar
}
func LeftSideBar() *container.AppTabs {
	tabs := container.NewAppTabs(
		container.NewTabItem("Tab 1", widget.NewLabel("Hello")),
		container.NewTabItem("Tab 2", widget.NewLabel("World!")),
	)
	return tabs
}

func sideBar(context context.Context) *fyne.Container {
	app := context.Value("app").(fyne.App)
	window := context.Value("currentW").(fyne.Window)

	sidebar := container.NewVBox(
		// widget.NewSeparator(),
		widget.NewButton("Hi!", func() {

		}),
		widget.NewButton("icon one!", func() {
			hello := widget.NewLabel("changing that prooooo")
			window.SetContent(Layout(context, hello))
		}),
		widget.NewButton("change content", func() {
			hello := widget.NewLabel("data changing brooo")
			window.SetContent(Layout(context, hello))
		}),
		widget.NewButton("close button", func() {
			app.Quit()
		}),
	)
	return sidebar
}
