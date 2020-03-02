import socket
from struct import pack
import cv2

HOST = "193.251.12.46"  # Standard loopback interface address (localhost)
PORT = 1111
#PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def main():
    print("Initializing...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        try:
            while True:
                data = clientsocket.recv(20)
                if not data:
                    break
                fps = unpack(">f", data[0:4])[0]
                width = unpack(">f", data[4:8])[0]
                height = unpack(">f", data[8:12])[0]
                size = unpack(">q", data[12:20])[0]

                print(fps, width, height, size)

                try:
                    data = read_from_socket(clientsocket, size)
                except ConnectionAbortedError:
                    break
                finally:
                    frame = numpy.ndarray(
                        (int(width), int(height), 3), dtype="uint8", buffer=data
                    )
                    print(frame)
                    cv2.imshow('frame', frame)

                    # Press Q on keyboard to exit
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break


            print("Client déconnecté...")

        except Exception as e:
            print("ERROR!", sys.exc_info())
        finally:
            cv2.destroyAllWindows()

    print("Done!")


if __name__ == "__main__":
    main()
