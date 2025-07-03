package Pages

import (
	"image/color"
	"log"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
	"github.com/Tjsingh01996/desktop/tcpUtil"
)

// Here we set meta for chat in the tab item
type tabMeta struct {
	currentChatUserId    string
	currentChatContainer *fyne.Container
	tabItem              *container.TabItem
}

// extend the fyne.TabItem to include a custom OnSelected function
var tabsHelper []*tabMeta

// To Search for a tab by user ID or tab ite
func findMetaByUserId(userId string) (*container.TabItem, *tabMeta) {
	for _, meta := range tabsHelper {
		if meta.currentChatUserId == userId {
			return meta.tabItem, meta
		}
	}
	return nil, nil
}

// To Search for a tab by tab item
func findMetaByTabItem(tabItem *container.TabItem) *tabMeta {
	for _, meta := range tabsHelper {
		if meta.tabItem == tabItem {
			return meta
		}
	}
	return nil
}

// onReceiveMessage listens for incoming messages and appends them to the chat container
func onReceiveMessage(messageCh chan tcpUtil.Message, sessionId string) {
	log.Printf("onReceiveMessage from %v ", currentChatUserId)
	for {
		message := <-messageCh
		log.Println("Received message: ", string(message.GetBody()), "To", message.GetHeader("To"), "From", message.GetHeader("From"))
		if message.GetHeader("To") == sessionId && message.GetHeader("From") == currentChatUserId {
			appendNewMessage(currentChatContainer, string(message.GetBody()))
		}
	}
}

// appendNewMessage appends a new message to the chat container with proper styling
func appendNewMessage(chatContainer *fyne.Container, message string) {
	maxWidth := 300.0
	messageLabel := widget.NewLabel(message)
	bgColor := color.NRGBA{200, 200, 200, 255} // Default gray for receiver
	align := fyne.TextAlignLeading
	messageLabel.Alignment = align
	bg := canvas.NewRectangle(bgColor)
	bg.CornerRadius = 24
	// Set the background size dynamically
	bg.SetMinSize(fyne.NewSize(float32(maxWidth), messageLabel.MinSize().Height+10))
	messageBox := container.NewMax(bg, container.NewPadded(messageLabel))
	chatContainer.Add(container.NewHBox(messageBox, layout.NewSpacer()))
}
