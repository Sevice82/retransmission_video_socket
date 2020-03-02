import socket
from struct import pack
import cv2

HOST = "193.251.12.46"  # Standard loopback interface address (localhost)
PORT = 1111
#PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

PATH_TO_VIDEO_FILE = "alcool.wmv"


def main():
    print("Initializing...")

    video_input = cv2.VideoCapture(PATH_TO_VIDEO_FILE)
    if not video_input.isOpened():
        print("ERROR: Unable to read video input feed")
        exit(1)

    print("Starting to read...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        try:
            while video_input.isOpened():
                ret, frame = video_input.read()
                print(type(frame), len(frame), frame.nbytes, video_input.get(cv2.CAP_PROP_FPS), video_input.get(cv2.CAP_PROP_FRAME_WIDTH), video_input.get(cv2.CAP_PROP_FRAME_HEIGHT))
                print(frame)

                if not ret or cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                """
                We add a header of 20 bytes before the actual frame.
                [   8  ][ 4][ 4][ 4][ ....... ]
                    |     |   |   |       \> frame
                    |     |   |   \> frame height
                    |     |   \> frame width
                    |     \> FPS
                    \> length of the whole message
                """
                header = bytearray()
                header += pack(">f", video_input.get(cv2.CAP_PROP_FPS))
                header += pack(">f", video_input.get(cv2.CAP_PROP_FRAME_WIDTH))
                header += pack(">f", video_input.get(cv2.CAP_PROP_FRAME_HEIGHT))
                header += pack(">q", frame.nbytes)

                sock.sendall(bytes(header))
                sock.sendall(frame)
        except Exception as e:
            import sys

            print("ERROR!", sys.exc_info())
        finally:
            # Release everything if job is finished
            video_input.release()
            cv2.destroyAllWindows()

    print("Done!")


if __name__ == "__main__":
    main()
