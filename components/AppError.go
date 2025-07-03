package components

import (
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/widget"
)

func ShowError(title string, e error, w fyne.Window) {
	content := container.NewVBox(
		widget.NewLabelWithStyle(title, fyne.TextAlignCenter, fyne.TextStyle{Bold: true}),
		widget.NewLabel(e.Error()),
	)
	dlg := dialog.NewCustom("Error", "OK", content, w)
	dlg.Show()
	go func() {
		<-time.After(2 * time.Second)
		dlg.Hide()
	}()
}
