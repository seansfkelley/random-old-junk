package matlab;

import com.mathworks.jmi.Matlab;

/**
 *
 * @author eullah01
 */
public class MatlabFEval extends MatlabRequest {

   private String command;
   private Object[] args;

   public MatlabFEval() {
   }

   public MatlabFEval(String command) {
      this(command, new Object[0]);
   }

   public MatlabFEval(String command, Object[] args) {
      this.command = command;
      this.args = args;
   }

   @Override
   protected void executeRequest() throws Exception {
      this.out.writeUTF(this.command);
      this.out.writeObject(this.args);
   }

   @Override
   protected void serveRequest(Matlab session) throws Exception {
      this.command = this.in.readUTF();
      this.args = (Object[]) this.in.readObject();
      session.feval(this.command, this.args, 0, this);
   }
}
