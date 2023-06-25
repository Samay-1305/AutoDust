# AutoDust

AutoDust is an IoT based program that can help in automatic waste segregation using a raspberry pi with a connected computer

## Working
- An AutoDust client first connects to a local server using sockets.
- The Socket is hosted on the users desktop/laptop.
- When the client detects an object, it snaps an Image and sends it to the local server.
- The local server then used YoloV3 to identify the object in the image.
- The classification is then classified as Biodegradable or Non-Biodegradable. This result is then set to the client.
- The client then segregates the waste based upon the received classifications
