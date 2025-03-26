package components

import (
	"fyne.io/fyne/v2/container"
)

type AppTabs struct {
	*container.AppTabs
}

func NewAppTabs(items ...*container.TabItem) *container.AppTabs {
	tabs := &container.AppTabs{}
	tabs.BaseWidget.ExtendBaseWidget(tabs)
	tabs.SetItems(items)
	return tabs
}
