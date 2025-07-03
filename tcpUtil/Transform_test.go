package tcpUtil

import "testing"

func TestEncodeMessage(t *testing.T) {
	headerKeys := []string{"key1", "key2"}
	header := map[string]any{headerKeys[0]: "helle how are you", headerKeys[1]: "im good"}
	// Create a sample Message
	msg := &Message{
		Header: header,
		Body:   []byte("Hello, World!"),
	}
	// Encode the message
	encoded := EncodeMessage(msg)
	// Decode the message
	decoded := DecodeMessage(encoded)
	// Check if the decoded message matches the original message
	for _, key := range headerKeys {
		if decoded.Header[key] != msg.Header[key] {
			t.Errorf("Expected %v, got %v", msg.Header[key], decoded.Header[key])
		}
	}
	if string(decoded.Body) != string(msg.Body) {
		t.Errorf("Expected %v, got %v", string(msg.Body), string(decoded.Body))
	}
	if len(decoded.Header) != len(msg.Header) {
		t.Errorf("Expected %v, got %v", len(msg.Header), len(decoded.Header))
	}
	if len(decoded.Body) != len(msg.Body) {
		t.Errorf("Expected %v, got %v", len(msg.Body), len(decoded.Body))
	}
}
