package components

import (
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
)

func CreateShadow(startColor ...color.NRGBA) *canvas.LinearGradient {
	sColor := color.NRGBA{0, 0, 0, 100}
	if len(startColor) > 0 {
		sColor = startColor[0]
	}
	gradient := canvas.NewLinearGradient(
		sColor,            // Darker at the start
		color.Transparent, // Fades to transparent
		0,                 // Direction of the shadow
	)
	gradient.SetMinSize(fyne.NewSize(300, 10))
	return gradient
}
