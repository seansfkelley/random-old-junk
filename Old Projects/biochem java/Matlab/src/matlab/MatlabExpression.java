package matlab;

import com.mathworks.jmi.Matlab;

/**
 *
 * @author eullah01
 */
public class MatlabExpression extends MatlabRequest {

   private String expression;

   protected MatlabExpression() {
   }

   public MatlabExpression(String expression) {
      this.expression = expression;
   }

   public String getExpression() {
      return expression;
   }

   @Override
   protected void executeRequest() throws Exception {
      this.out.writeUTF(this.expression);
   }

   @Override
   protected void serveRequest(Matlab session) throws Exception {
      this.expression = this.in.readUTF();
      session.eval(expression, this);
   }
}
