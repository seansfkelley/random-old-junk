package matlab;

import com.mathworks.jmi.Matlab;
import com.mathworks.jmi.MatlabEvent;
import com.mathworks.jmi.MatlabListener;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.SocketTimeoutException;

/**
 *
 * @author eullah01
 */
public abstract class MatlabRequest implements MatlabListener {
   private static final int TIMEOUT_MS = 5000;

   private static InetAddress address;
   private static int port;

   static {
      MatlabRequest.setServer(MatlabServer.address, MatlabServer.port);
   }
   private Socket socket;
   protected ObjectInputStream in;
   protected ObjectOutputStream out;
   protected MatlabResponseType responseType;
   protected int status;
   protected Object result;

   public static void setServer(InetAddress address, int port) {
      MatlabRequest.address = address;
      MatlabRequest.port = port;
   }

   protected MatlabRequest() {
      this.responseType = MatlabResponseType.NONE;
   }

   public int getStatus() {
      return status;
   }

   public Object getResult() {
      return result;
   }

   public MatlabResponseType getResponseType() {
      return this.responseType;
   }

   protected void setResponseType(int type) {
      switch (type) {
         case MatlabEvent.MATLAB_CTRLC:
            this.responseType = MatlabResponseType.CTRL_C;
            break;
         case MatlabEvent.MATLAB_QUITTING:
            this.responseType = MatlabResponseType.QUITING;
            break;
         case MatlabEvent.MATLAB_REPLY:
            this.responseType = MatlabResponseType.REPLY;
            break;
         default:
            this.responseType = MatlabResponseType.NONE;
      }
   }

   private void connect() throws Exception {
      this.socket = new Socket(address, port);
      this.socket.setSoTimeout(MatlabRequest.TIMEOUT_MS);
      this.out = new ObjectOutputStream(this.socket.getOutputStream());
      this.out.flush();
      this.in = new ObjectInputStream(this.socket.getInputStream());
   }

   public void execute() throws Exception {
      this.connect();
      Exception exception = null;
      try {
         this.out.writeUTF(this.getClass().getCanonicalName());
         this.out.flush();
         this.executeRequest();
         this.out.flush();
         this.setResponseType(this.in.readInt());
         this.status = this.in.readInt();
         this.result = this.in.readObject();
      }
      catch (SocketTimeoutException ste){
         exception = ste;
         this.responseType = MatlabResponseType.ERROR;
      }
      catch (Exception e) {
         e.printStackTrace();
         exception = e;
         this.responseType = MatlabResponseType.ERROR;
      }
      this.socket.close();
      if (exception != null) {
         throw exception;
      }
   }

   public static void serve(Socket socket, Matlab session) throws Exception {
      ObjectInputStream in = new ObjectInputStream(socket.getInputStream());
      ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
      out.flush();
      Class cls = Class.forName(in.readUTF());
      if (MatlabRequest.class.isAssignableFrom(cls)) {
         MatlabRequest request = (MatlabRequest) cls.newInstance();
         request.socket = socket;
         request.in = in;
         request.out = out;
         request.serveRequest(session);
         out.flush();
      }
   }

   @Override
   public void matlabEvent(MatlabEvent event) {
      try {
         this.out.writeInt(event.getEventType());
         this.out.writeInt(event.getStatus());
         this.out.writeObject(event.getResult());
         this.out.flush();
      } catch (Exception ex) {
         ex.printStackTrace();
      }
   }

   protected abstract void executeRequest() throws Exception;

   protected abstract void serveRequest(Matlab session) throws Exception;
}
