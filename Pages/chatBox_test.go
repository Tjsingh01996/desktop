package Pages

import (
	"context"
	"testing"
)

func TestChatBox(t *testing.T) {
	ctx := context.Background()
	ctx = context.WithValue(ctx, "currentUser", map[string]interface{}{
		"id":    "2e8acbd4-2272-4917-be15-34d0a807cc69",
		"name":  "Test User",
		"email": "tejveer.singh@simsaw.com",
	})

	chatBox := ChatBox(ctx)
	if chatBox == nil {
		t.Error("ChatBox returned nil container")
	} else {
		t.Log("ChatBox returned a valid container")
	}
	length := len(chatBox.Objects)
	if length != 2 {
		t.Errorf("ChatBox container has %d objects, expected 2", length)
	} else {
		t.Logf("ChatBox container has %d objects as expected", length)
	}
	if length == 0 {
		t.Error("ChatBox container has no objects")
	} else {
		t.Logf("ChatBox container has %d objects", length)
	}
}
