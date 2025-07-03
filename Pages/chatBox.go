package Pages

import (
	"context"
	"fmt"
	"image/color"
	"log"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
	clientserver "github.com/Tjsingh01996/desktop/clientServer"
	"github.com/Tjsingh01996/desktop/components"
	"github.com/Tjsingh01996/desktop/services/messages"
	"github.com/Tjsingh01996/desktop/tcpUtil"
)

var chatList *messages.ChatList
var currentChatContainer *fyne.Container
var currentChatUserId string
var chatServer *clientserver.ClientsServer

// ChatBox creates a chat box UI with a list of chats and a message input area
func ChatBox(ctx context.Context) *fyne.Container {
	chatList = messages.NewChatList()
	currentUser := ctx.Value("currentUser").(map[string]interface{})
	chatServer = clientserver.NewClientsServer(currentUser["id"].(string))

	err := chatServer.Connect()
	if err != nil {
		panic(err)
	}
	var tabItems = make([]*container.TabItem, 0)
	tabs := []struct {
		Text              string
		currentChatUserId string
		content           fyne.CanvasObject
	}{
		{
			Text:              "tejveer.singh01996@gmail.com",
			currentChatUserId: "1e586641-09bc-45fe-bc94-1352dde6372a",
		},
		{
			Text:              "tejveer.singh@simsaw.com",
			currentChatUserId: "2e8acbd4-2272-4917-be15-34d0a807cc69",
		},
		{
			Text:    "Tab 2",
			content: widget.NewLabel("World!"),
		},
	}
	for _, tab := range tabs {
		if currentUser["id"] == tab.currentChatUserId {
			continue // Skip the current user
		}
		tabMeta := &tabMeta{
			currentChatUserId:    tab.currentChatUserId,
			currentChatContainer: nil,
		}
		tabsHelper = append(tabsHelper, tabMeta)
		if tab.content == nil {
			tab.content = container.NewVScroll(CreateChatUI(ctx, tab.currentChatUserId))
		}
		tabItem := container.NewTabItem(tab.Text, tab.content)
		tabMeta.tabItem = tabItem
		tabItems = append(tabItems, tabItem)
	}
	messageCha := make(chan tcpUtil.Message)
	go chatServer.Listener(messageCha)
	currentChatContainer = tabsHelper[0].currentChatContainer
	currentChatUserId = tabsHelper[0].currentChatUserId
	go onReceiveMessage(messageCha, currentUser["id"].(string))
	pageContent := components.NewAppTabs(
		tabItems...,
	)
	//@TODO need to be optimized
	pageContent.OnSelected = func(selected *container.TabItem) {
		if meta := findMetaByTabItem(selected); meta != nil {
			currentChatUserId = meta.currentChatUserId
			currentChatContainer = meta.currentChatContainer
		}
	}
	pageContent.SetTabLocation(container.TabLocationLeading)
	content := container.New(layout.NewStackLayout(), pageContent)
	return content
}

func CreateChatUI(ctx context.Context, currentChatUserId string) *fyne.Container {
	fmt.Printf("Creating chat UI for chatId: %s and type  %T\n", ctx.Value("currentUser"), ctx.Value("currentUser"))
	defer func() {
		log.Println("exit chat ")
	}()

	messages := chatList.GetMessages(currentChatUserId)
	maxWidth := 300.0

	chatContainer := container.NewVBox()
	_, chatMeta := findMetaByUserId(currentChatUserId)
	if chatMeta == nil {
		panic(fmt.Sprintf("No chat meta found for userId: %s", currentChatUserId))
	}
	chatMeta.currentChatContainer = chatContainer
	for _, msg := range messages {
		messageLabel := widget.NewLabel(msg.Text)
		messageLabel.Wrapping = fyne.TextWrapWord

		// Background color for messages
		bgColor := color.NRGBA{200, 200, 200, 255} // Default gray for receiver
		align := fyne.TextAlignLeading

		if msg.IsSender {
			bgColor = color.NRGBA{0, 122, 255, 255} // Blue for sender
			align = fyne.TextAlignLeading
		}

		messageLabel.Alignment = align
		bg := canvas.NewRectangle(bgColor)
		bg.CornerRadius = 24
		// Set the background size dynamically
		bg.SetMinSize(fyne.NewSize(float32(maxWidth), messageLabel.MinSize().Height+10))
		messageBox := container.NewMax(bg, container.NewPadded(messageLabel))

		if msg.IsSender {
			chatContainer.Add(container.NewHBox(layout.NewSpacer(), messageBox))
		} else {
			chatContainer.Add(container.NewHBox(messageBox, layout.NewSpacer()))
		}
	}
	scrollChat := container.NewVScroll(chatContainer)
	scrollChat.SetMinSize(fyne.NewSize(400, 400))
	userNameInput := components.NewInput()
	userNameInput.SetMinSize(fyne.NewSize(400, 50))
	userNameInput.SetPlaceHolder("Type your message...")
	onSubmit := func(text string) {
		messageLabel := widget.NewLabel(userNameInput.Text)
		bgColor := color.NRGBA{0, 122, 255, 255} // Blue for sender
		align := fyne.TextAlignLeading
		messageLabel.Alignment = align
		bg := canvas.NewRectangle(bgColor)
		bg.CornerRadius = 24
		chatServer.SendMessageToServer(currentChatUserId, []byte(userNameInput.Text))
		// Set the background size dynamically
		bg.SetMinSize(fyne.NewSize(float32(maxWidth), messageLabel.MinSize().Height+10))
		messageBox := container.NewMax(bg, container.NewPadded(messageLabel))
		chatContainer.Add(container.NewHBox(layout.NewSpacer(), messageBox))

		userNameInput.SetText("")
		// clientserver.SendMessageToServer()
		scrollChat.ScrollToBottom()
	}

	userNameInput.OnSubmitted = onSubmit
	form := widget.NewForm(
		widget.NewFormItem("", userNameInput),
	)
	form.OnSubmit = func() {
		onSubmit("")
	}
	inputForm := form
	finalLayout := container.NewBorder(nil, inputForm, nil, nil, scrollChat)

	return finalLayout // Scrollable chat area
}
