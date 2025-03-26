package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
)

func main12() {
	myApp := app.New()
	myWindow := myApp.NewWindow("Centered Form")

	// Creating form fields
	nameEntry := widget.NewEntry()
	ageEntry := widget.NewEntry()

	// Wrapping entries in containers to set minimum size
	nameContainer := container.NewHBox(layout.NewSpacer(), nameEntry, layout.NewSpacer())
	ageContainer := container.NewHBox(layout.NewSpacer(), ageEntry, layout.NewSpacer())
	// nameContainer.Resize()
	// Setting a fixedsize using AdaptiveGrid
	form := container.NewVBox(
		widget.NewLabel("Name"),
		container.NewAdaptiveGrid(1, nameContainer), // Ensures field stretches
		widget.NewLabel("Age"),
		container.NewAdaptiveGrid(1, ageContainer),
		widget.NewButton("Submit", func() {
			// Handle form submission
		}),
	)

	// Wrapping form in a centered container
	centeredForm := container.NewCenter(form)

	myWindow.SetContent(centeredForm)
	myWindow.Resize(fyne.NewSize(400, 300)) // Set window size
	myWindow.ShowAndRun()
}
