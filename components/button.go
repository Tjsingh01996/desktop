package components

import "fyne.io/fyne/v2/widget"

type Button struct {
	component *widget.Button
}

func InitiateButton(label string) *Button {
	return &Button{
		component: widget.NewButton(label, func() {}),
	}
}
func (b *Button) Disable() {
	b.component.Disable()
}
func (b *Button) Disabled() bool {
	return b.component.Disabled()
}

func (b *Button) Enable() {
	b.component.Enable()
}

func (b *Button) setText(text string) {
	b.component.SetText(text)
}
