package matlab;

/**
 *
 * @author eullah01
 */
public class Main {
   private static String exp = "[t, y] = ode45(\'react\', [0 10], [2 .1 .5 1]);";

   public static void main(String[] args) throws Exception {
      testExpression();
   }

   private static void testFEval() throws Exception {
      MatlabFEval feval = new MatlabFEval("sqrt", new Integer[]{9});
      feval.execute();
      System.out.println("Type : " + feval.getResponseType());
      System.out.println("Stat : " + Integer.toHexString(feval.getStatus()));
      Object result = feval.getResult();
      System.out.println(result.getClass());
      double[] res = (double[]) result;
      System.out.println(res.length);
      System.out.println(res[0]);
      System.out.flush();
   }

   private static void testExpression() throws Exception {
      MatlabExpression expression = new MatlabExpression(exp);
      expression.execute();
      System.out.println("Type : " + expression.getResponseType());
      System.out.println("Stat : " + Integer.toHexString(expression.getStatus()));
      System.out.println(expression.getResult());
      System.out.flush();
   }
}
