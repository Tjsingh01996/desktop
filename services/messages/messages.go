package messages

type ChatList struct {
	chats map[string][]struct {
		Text     string
		IsSender bool
	}
}

// NewChatList creates a new ChatList instance
func NewChatList() *ChatList {
	return &ChatList{
		chats: make(map[string][]struct {
			Text     string
			IsSender bool
		}),
	}
}

// getChatList retrieves the chat list for a given chat ID
func (c *ChatList) GetMessages(chatID string) []struct {
	Text     string
	IsSender bool
} {
	if chat, ok := c.chats[chatID]; ok {
		return chat
	} else {
		// create a new chat list if it doesn't exist
		c.chats[chatID] = []struct {
			Text     string
			IsSender bool
		}{}
		return c.chats[chatID]
	}
}

func (c *ChatList) addChat(chatID string, text string, isSender bool) {
	if _, ok := c.chats[chatID]; !ok {
		c.chats[chatID] = []struct {
			Text     string
			IsSender bool
		}{}
	}
	c.chats[chatID] = append(c.chats[chatID], struct {
		Text     string
		IsSender bool
	}{Text: text, IsSender: isSender})
}
