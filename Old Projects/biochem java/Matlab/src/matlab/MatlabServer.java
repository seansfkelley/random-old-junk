package matlab;

import com.mathworks.jmi.Matlab;
import java.net.InetAddress;
import java.net.ServerSocket;

public class MatlabServer extends Thread {

   protected static InetAddress address = null;
   protected static int port = 2107;

   static {
      try {
         address = InetAddress.getLocalHost();
      } catch (Exception exception) {
      }
   }
   private Matlab matlab;
   private ServerSocket server;

   public MatlabServer() throws Exception {
      this.matlab = new Matlab();
   }

   public void serve() throws Exception {
      if (this.server == null) {
         this.server = new ServerSocket(port, 10, address);
      }
      new MatlabServerConnection(matlab, this.server.accept()).start();
   }

   @Override
   public void run() {
      try {
         while (true) {
            this.serve();
         }
      } catch (Exception e) {
      }
   }

   @Override
   public void finalize() {
      try {
         this.stopServer();
      } catch (Exception e) {
      }
   }

   public void stopServer() throws Exception {
      this.server.close();
      this.server = null;
   }
}
