package main

import (
	"context"
	"fmt"
	"net"
	"time"
	"github.com/mdlayher/vsock"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type vsockDialer struct {
	addr *vsock.Addr
}

func (d *vsockDialer) dial(ctx context.Context, _ string) (net.Conn, error) {
	// The newer vsock.Dial accepts (cid, port, *vsock.Config)
	return vsock.Dial(d.addr.ContextID, d.addr.Port, nil)
}

func main() {
	addr := &vsock.Addr{ContextID: 2, Port: 9999}
	dialer := &vsockDialer{addr: addr}

	grpcOpts := []grpc.DialOption{
		grpc.WithContextDialer(dialer.dial),
		grpc.WithTransportCredentials(insecure.NewCredentials()), // use insecure instead of WithInsecure
	}

	fmt.Println("Starting gRPC probe on VSOCK 2:9999...")
	for {
		// using grpc.NewClient is preferred in new grpc, but Dial works.
		conn, err := grpc.Dial(addr.String(), grpcOpts...)
		if err == nil {
			fmt.Println("[!] CONNECTION SUCCESS: gRPC Handshake accepted by CID 2")
			conn.Close()
		} else {
            fmt.Println("Failed:", err)
        }
		time.Sleep(500 * time.Millisecond)
	}
}
