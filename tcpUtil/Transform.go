package tcpUtil

import (
	"bytes"
	"encoding/gob"
	"log"
)

func EncodeMessage(data *Message) *bytes.Buffer {
	buf := new(bytes.Buffer)
	enc := gob.NewEncoder(buf)
	err := enc.Encode(data)
	if err != nil {
		log.Fatal("encode error:", err)
	}
	return buf
}

func DecodeMessage(payload *bytes.Buffer) Message {
	dec := gob.NewDecoder(payload)
	var data Message
	err := dec.Decode(&data)
	if err != nil {
		log.Fatal("decode error:", err)
	}
	return data
}

const (
	skip = iota
	ChatNotFound
	MessageSent
)

type Message struct {
	Header map[string]any
	Body   []byte
}

func NewMessage(body []byte) Message {
	return Message{
		Header: make(map[string]any),
		Body:   body,
	}
}

func (message *Message) SetHeader(key string, value any) {
	if message.Header == nil {
		message.Header = make(map[string]any)
	}
	message.Header[key] = value
}

func (message *Message) GetHeader(key string) any {
	if message.Header == nil {
		return ""
	}
	return message.Header[key]
}

func (message *Message) deleteHeaderKey(key string) {
	if message.Header == nil {
		return
	}
	delete(message.Header, key)
}
func (message *Message) GetBody() []byte {
	if message.Body == nil {
		return nil
	}
	return message.Body
}
