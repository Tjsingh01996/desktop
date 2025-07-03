package https

import (
	"fmt"
	"log"
	"net"
)

type SeverConfig struct {
}
type tcp struct {
	listener               net.Listener
	onConnectNewConnection func(net.Conn) error
}

func NewTcp() *tcp {
	return &tcp{}
}

func (t *tcp) SetOnConnectNewConnection(function func(net.Conn) error) {
	t.onConnectNewConnection = function
}

func (t *tcp) Serve(port uint16) error {
	str := fmt.Sprintf(":%v", port)
	listener, err := net.Listen("tcp", str)
	defer listener.Close()
	if err != nil {
		return err
	}
	log.Printf("server start on %v", port)
	t.listener = listener
	t.accept()
	return nil
}

func (t *tcp) accept() {
	for {
		conn, err := t.listener.Accept()
		if err != nil {
			log.Print(err)
			handleError(err)
			return
		}
		if t.onConnectNewConnection != nil {
			go t.onConnectNewConnection(conn)
		}
		if err != nil {
			handleError(err)
		}
		go handleConnection(conn)
	}

}

func handleConnection(conn net.Conn) {
	return
}

// handle error it encounter while requesting
func handleError(err error) {
	log.Print(err, "here is error br")
}
