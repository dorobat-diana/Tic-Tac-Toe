import java.io.*;
import java.net.Socket;
import java.util.Scanner;

public class Client {

    private Socket socket;
    private BufferedReader reader;
    private BufferedWriter writer;

    public Client(Socket socket) {
        try {
            this.socket = socket;
            this.reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            this.writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
        } catch (IOException e) {
            closeEverything(socket, reader, writer);
        }
    }

    public void sendMessage(String m) {
        try {
            int random1 = (int)(Math.random() * 3);
            int random2 = (int)(Math.random() * 3);
            String message = random1 + ","+ random2 ;
            writer.write(message);
            writer.newLine();
            writer.flush();
        } catch (IOException e) {
            closeEverything(socket, reader, writer);
        }
    }

    public void listenForGameUpdates() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                String messageFromServer;
                while (socket.isConnected()) {
                    try {
                        messageFromServer = reader.readLine();
                        if (messageFromServer == null) {
                            closeEverything(socket, reader, writer);
                            break;
                        }
                        System.out.println(messageFromServer);
                        sendMessage("");
                    } catch (IOException e) {
                        closeEverything(socket, reader, writer);
                    }
                }
            }
        }).start();
    }

    public void closeEverything(Socket socket, BufferedReader reader, BufferedWriter writer) {
        try {
            if (reader != null) {
                reader.close();
            }
            if (writer != null) {
                writer.close();
            }
            if (socket != null) {
                socket.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        try {
            Scanner scanner = new Scanner(System.in);
            Socket socket = new Socket("172.30.115.97", 12345); // Replace with your server address and port
            Client client = new Client(socket);

            // Initialize the game here

            client.listenForGameUpdates();

            client.sendMessage("");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
