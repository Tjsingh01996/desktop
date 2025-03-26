package main

import (
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/theme"
)

type AppTheme struct {
	fyne.Theme
	variant fyne.ThemeVariant
}

func newAppTheme(variant fyne.ThemeVariant) *AppTheme {
	return &AppTheme{
		Theme:   theme.DefaultTheme(),
		variant: variant,
	}
}

func (f *AppTheme) Color(name fyne.ThemeColorName, _ fyne.ThemeVariant) color.Color {
	return f.Theme.Color(name, f.variant)
}

func (c AppTheme) Size(name fyne.ThemeSizeName) float32 {
	switch name {
	case theme.SizeNamePadding:
		return 16 // Increase padding
	default:
		return c.Theme.Size(name)
	}
}
