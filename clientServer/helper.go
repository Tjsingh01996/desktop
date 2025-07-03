package clientserver

import (
	"encoding/gob"
	"log"

	"github.com/Tjsingh01996/desktop/tcpUtil"
)

func ReadFromConn(dec *gob.Decoder) (tcpUtil.Message, error) {

	var data tcpUtil.Message
	err := dec.Decode(&data)
	if err != nil {
		log.Println("Read error:", err)
		return tcpUtil.Message{}, err
	}
	return data, nil
}

func WriteOnConn(enc *gob.Encoder, data tcpUtil.Message) error {

	err := enc.Encode(data)
	if err != nil {
		log.Println("Write error:", err)
		return err
	}

	return nil
}
