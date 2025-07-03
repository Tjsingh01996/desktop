package clientserver

import (
	"encoding/gob"
	"log"
	"net"

	"github.com/Tjsingh01996/desktop/tcpUtil"
)

type ClientsServer struct {
	port         uint16
	conn         net.Conn
	ConnectionId string
	SessionId    string
	encoder      *gob.Encoder
	decoder      *gob.Decoder
}

// NewClientsServer creates a new ClientsServer instance
func NewClientsServer(sessionId string) *ClientsServer {
	return &ClientsServer{
		SessionId: sessionId,
	}
}
func (server *ClientsServer) Connect() error {
	if server.conn == nil {
		connectionToSever, err := net.Dial("tcp", "localhost:8000")
		if err != nil {
			log.Print(err)
			return err
		}
		server.conn = connectionToSever
		enc := gob.NewEncoder(server.conn)
		decoder := gob.NewDecoder(server.conn)
		log.Println("Connected to server on port:", server.conn)
		server.encoder = enc
		server.decoder = decoder
		server.handShake()
		return nil
	}
	return nil
}

func (server *ClientsServer) SendMessageToServer(userId string, messageBytes []byte) error {

	messageToSend := tcpUtil.NewMessage(messageBytes)
	messageToSend.SetHeader("To", userId)
	err := WriteOnConn(server.encoder, messageToSend)
	if err != nil {
		log.Println("Write error:", err)
		return err
	}
	return nil
}

func (server *ClientsServer) handShake() {
	message, err := ReadFromConn(server.decoder)
	if err != nil {
		log.Println("Handshake error:", err)
		return
	}
	if message.GetHeader("ACK") != 1 {
		sendMessage := tcpUtil.NewMessage([]byte("Hello, server!"))
		sendMessage.SetHeader("ACK", 0)
		server.conn.Close()
		WriteOnConn(server.encoder, sendMessage)
		server.conn.Close()
		log.Println("Handshake failed, ACK not received")
		return
	}

	if message.GetHeader("ChatId") == nil {
		log.Println("Handshake failed, ChatId not received")
		sendMessage := tcpUtil.NewMessage([]byte("Hello, server!"))
		sendMessage.SetHeader("ACK", 0)
		server.conn.Close()
		WriteOnConn(server.encoder, sendMessage)
		return
	}

	sendMessage := tcpUtil.NewMessage([]byte("Hello, server!"))
	sendMessage.SetHeader("ACK", 1)
	sendMessage.SetHeader("sessionId", server.SessionId)
	WriteOnConn(server.encoder, sendMessage)
	responseMessage, err := ReadFromConn(server.decoder)
	if responseMessage.GetHeader("ACK") == 2 {
		log.Println("Handshake ACK received")
	} else {
		server.conn.Close()
		return
	}
	server.ConnectionId = message.GetHeader("ChatId").(string)
	log.Println("Handshake successful, ChatId:", server.ConnectionId)
}

func (server *ClientsServer) Listener(messagCh chan tcpUtil.Message) {
	if server.conn == nil {
		log.Println("No connection to server.")
		return
	}
	decoder := server.decoder
	for {
		log.Println("Listening for messages...")
		var message tcpUtil.Message
		err := decoder.Decode(&message)
		if err != nil {
			log.Println("Read error:", err)
			break
		}
		log.Printf("Message Listener body: %v, from: %v, status: %v", string(message.Body), message.GetHeader("From"), message.GetHeader("Status"))
		messagCh <- message
	}
}
