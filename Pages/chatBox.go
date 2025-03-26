package Pages

import (
	"context"
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
	"github.com/Tjsingh01996/desktop/components"
)

func ChatBox(ctx context.Context) *fyne.Container {
	pageContent := components.NewAppTabs(
		container.NewTabItem("alksdlkds", container.NewVScroll(CreateChatUI())),
		container.NewTabItem("Tab 2", widget.NewLabel("World!")),
	)

	pageContent.SetTabLocation(container.TabLocationLeading)
	content := container.New(layout.NewStackLayout(), pageContent)

	return content
}

func CreateChatUI() *fyne.Container {
	// Dummy chat messages
	messages := []struct {
		text     string
		isSender bool
	}{
		{"hello", true},
		{"hello", false},
		{"hello", true},
		{"hello", false},
		{"hello", false},
		{"hello", false},
		{"Yrr ke ha ye .akjsdkjaskjdhljkahsdkjhakjsdhkjahsdkljhakjshdjk", true},
		{"hello", false},
		{"hello", false},
		{"hello", false},
		{"hello", false},
		{"hello", false},
		{"hello", false},
		{"Yrr ke ha ye .akjsdkjaskjdhljkahsdkjhakjsdhkjahsdkljhakjshdjk", true},
		{"hello", false},
		{"hello", false},
		{"Yrr ke ha ye .akjsdkjaskjdhljkahsdkjhakjsdhkjahsdkljhakjshdjk", true},
		{"hello", false},
	}

	chatContainer := container.NewVBox()

	maxWidth := 300.0 // Set max width for labels

	for _, msg := range messages {
		messageLabel := widget.NewLabel(msg.text)
		messageLabel.Wrapping = fyne.TextWrapWord

		// Background color for messages
		bgColor := color.NRGBA{200, 200, 200, 255} // Default gray for receiver
		align := fyne.TextAlignLeading

		if msg.isSender {
			bgColor = color.NRGBA{0, 122, 255, 255} // Blue for sender
			align = fyne.TextAlignLeading
		}

		messageLabel.Alignment = align
		bg := canvas.NewRectangle(bgColor)
		bg.CornerRadius = 24

		// Set the background size dynamically
		bg.SetMinSize(fyne.NewSize(float32(maxWidth), messageLabel.MinSize().Height+10))

		messageBox := container.NewMax(bg, container.NewPadded(messageLabel))

		if msg.isSender {
			chatContainer.Add(container.NewHBox(layout.NewSpacer(), messageBox))
		} else {
			chatContainer.Add(container.NewHBox(messageBox, layout.NewSpacer()))
		}
	}
	return chatContainer // Scrollable chat area
}

// func CreateChatUI() *fyne.Container {

// 	// Dummy chat messages
// 	messages := []struct {
// 		Text   string
// 		Sender string // "Me" or "Friend"
// 	}{
// 		{"Hey! How are you ?", "Friend"},
// 		{"I'm good, how about you?", "Me"},
// 		{"I'm doing great! What are you up to?", "Friend"},
// 		{"Just coding a chat app in Fyne 😃", "Me"},
// 		{"Wow! That sounds cool!", "Friend"},
// 		{"Wow! That sounds cool!", "Friend"},
// 	}

// 	// Chat history container
// 	chatList := container.NewVBox()

// 	// Add dummy messages with full-width alignment
// 	for _, msg := range messages {
// 		msgLabel := widget.NewLabel(msg.Text)

// 		// msgLabel := container.NewHBox(label)
// 		msgLabel.Wrapping = fyne.TextWrapWord // Enable word wrap

// 		// Background color for message bubbles
// 		var bgColor color.Color
// 		var msgContainer *fyne.Container

// 		if msg.Sender == "Me" {
// 			bgColor = theme.Color(theme.ColorNamePrimary) // Primary color for "Me"
// 			bg := canvas.NewRectangle(bgColor)
// 			msgContainer = container.NewHBox(widget.NewLabel(""), msgLabel)
// 			msgContainer = container.NewBorder(nil, nil, nil, layout.NewSpacer(),
// 				container.NewStack(bg, container.NewPadded(msgLabel)),
// 			)
// 			msgContainer.Resize(fyne.NewSize(100, 100))
// 		} else {
// 			bgColor = color.RGBA{200, 200, 200, 255} // Light gray for "Friend"
// 			bg := canvas.NewRectangle(bgColor)
// 			msgContainer = container.NewBorder(nil, nil, layout.NewSpacer(), nil,
// 				container.NewStack(bg, container.NewPadded(msgLabel)),
// 			)
// 			msgContainer.Resize(fyne.NewSize(100, 100))
// 		}

// 		chatList.Add(msgContainer)
// 	}

// 	// Ensure it expands inside the tab properly
// 	return chatList
// 	// // Scrollable chat area

// }
