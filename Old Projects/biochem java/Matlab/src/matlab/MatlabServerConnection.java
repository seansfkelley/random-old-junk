package matlab;

import com.mathworks.jmi.Matlab;
import java.net.Socket;

/**
 *
 * @author eullah01
 */
public class MatlabServerConnection extends Thread {

   private Matlab session;
   private Socket connection;

   public MatlabServerConnection(Matlab session, Socket connection) {
      this.session = session;
      this.connection = connection;
   }

   @Override
   public void run() {
      try {
         MatlabRequest.serve(this.connection, this.session);
      } catch (Exception e) {
         e.printStackTrace();
      }
   }
}
