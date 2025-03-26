package layouts

import (
	"fyne.io/fyne/v2"
)

const sideWidth = 220

type AppLayout struct {
	top, left, right, content fyne.CanvasObject
}

func NewAppLayout(top, left, right, content fyne.CanvasObject) fyne.Layout {
	return &AppLayout{
		top:     top,
		left:    left,
		right:   right,
		content: content,
	}
}

func (layout *AppLayout) Layout(objects []fyne.CanvasObject, size fyne.Size) {
	topHeight := layout.top.MinSize().Height
	if layout.top != nil {
		layout.top.Resize(fyne.NewSize(size.Width, topHeight))
	}
	if layout.left != nil {
		layout.left.Move(fyne.NewPos(0, topHeight))
		layout.left.Resize(fyne.NewSize(sideWidth, size.Height-topHeight))
	}
	if layout.right != nil {
		layout.right.Move(fyne.NewPos(size.Width-sideWidth, topHeight))
		layout.right.Resize(fyne.NewSize(sideWidth, size.Height-topHeight))
	}
	if layout.content != nil {
		layout.content.Move(fyne.NewPos(sideWidth, topHeight))
		layout.content.Resize(fyne.NewSize(size.Width-sideWidth, size.Height-topHeight))
	}
}

func (layout *AppLayout) SetContent(obj fyne.CanvasObject) {
	layout.content = obj
	// layout.content.Refresh()
}

func (layout *AppLayout) MinSize(objects []fyne.CanvasObject) fyne.Size {
	return fyne.NewSize(1024, 1024)
}
