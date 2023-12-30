import java.io.*;
import java.net.*;
import java.util.Scanner;

public class UDPClient {

    private DatagramSocket socket;
    private InetAddress serverAddress;
    private int serverPort;

    public UDPClient(String serverAddress, int serverPort) {
        try {
            this.socket = new DatagramSocket();
            this.serverAddress = InetAddress.getByName(serverAddress);
            this.serverPort = serverPort;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void sendMessage(String message) {
        try {
            byte[] data = message.getBytes();
            DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, serverPort);
            socket.send(packet);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void listenForGameUpdates() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                byte[] buffer = new byte[1024];
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);

                while (true) {
                    try {
                        socket.receive(packet);
                        String messageFromServer = new String(packet.getData(), 0, packet.getLength());
                        System.out.println(messageFromServer);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();
    }

    public static void main(String[] args) {
        try {
            Scanner scanner = new Scanner(System.in);
            UDPClient client = new UDPClient("172.30.115.97", 12345); // Replace with your server address and port

            // Initialize the game here

            client.listenForGameUpdates();

            while (true) {
                // Implement your game logic and user input handling here
                String userInput = scanner.nextLine();
                client.sendMessage(userInput);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
