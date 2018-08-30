package biochem;

import java.io.*;
import java.net.*;
import java.util.*;
import java.util.regex.*;
import matlab.*;
import org.jgap.*;

public class GeneralFormMatlabFitness extends DataBasedFitnessFunction{

  private static final String
          VAR_ODE_SOLUTION =    GAParameters.MATLAB_VAR_ODE_SOLUTION,
          VAR_ODE_PARAM =       GAParameters.MATLAB_VAR_ODE_PARAM,
          VAR_ERROR =           "ERROR_VALUE",

          CONST_TIMESTEPS =     "ANSWER_T",
          CONST_ODE_SOLUTION =  "ANSWER_" + VAR_ODE_SOLUTION,
          CONST_INIT_CONC =     "INIT_CONCENTRATIONS",
          CONST_NUM_ODES =      "NUM_ODES",
          CONST_NUM_DATASETS =  "NUM_DATASETS",
          CONST_NUM_PARAMS =    "NUM_PARAMS",
          CONST_NUM_CONSTANTS = "NUM_CONSTANTS",
          CONST_ODE_OPTS =      "ODE_OPTIONS",
          CONST_NOISE =         "NOISE_PCT",
          CONST_COLORS =        "PLOT_COLORS",

          FUNC_ODE_SOLVER =     "ode15s",
          FUNC_ODE =            "ode",
          FUNC_EXEC_ODE =       "react_ode_all",
          FUNC_INIT_ODE =       "init_ode",
          FUNC_ERROR =          "average_error",
          FUNC_NOISE =          "noise",

          FILE_PATH =           "/Users/sk/Documents/MATLAB/",
          SCRIPT_INITIALIZE =   "initialize_constants",
          CMD_INIT_MATLAB =     "/Applications/MATLAB_R2008bSV.app/bin/matlab -nodesktop -nodisplay -r server",
          MATLAB_ERROR =        "MATLAB_ERROR";

  private static final String MATCH_NUMBER_REGEX =       "([-+]?\\p{Digit}+(\\.\\p{Digit}+)?(e[-+]\\p{Digit}+)?)|(Inf)|(NaN)",
                              MATCH_ERROR_ASSIGN_REGEX = VAR_ERROR + ".*=.*" + MATCH_NUMBER_REGEX;

  private static final Pattern MATCH_NUMBER = Pattern.compile(MATCH_NUMBER_REGEX, Pattern.DOTALL),
                               MATCH_ERROR_ASSIGN = Pattern.compile(MATCH_ERROR_ASSIGN_REGEX, Pattern.DOTALL);

  private static final int RETRY_WAIT_MS = 2000, MAX_RETRIES = 20;

  private String ode_command, error_command;
  private File mfile;
  private boolean answer_t_set, answer_var_set;
  private Process matlab_process;
  private ShutdownThread shutdown_comms;

  public GeneralFormMatlabFitness(double[][] init_concentrations, GeneralFormGene gfg) {
    answer_t_set = answer_var_set = false;
    mfile = new File(FILE_PATH + FUNC_ODE + ".m");

    ode_command = VAR_ODE_SOLUTION + " = " + FUNC_EXEC_ODE + "(\'" + FUNC_ODE + "\');";
    error_command = VAR_ERROR + " = " + FUNC_ERROR + "(" + VAR_ODE_SOLUTION + ", " +
            CONST_ODE_SOLUTION + ")"; // No semicolon! Prints answer.

    File init_script = new File(FILE_PATH + SCRIPT_INITIALIZE + ".m");

    // <editor-fold defaultstate="collapsed" desc="Write INIT_SCRIPT.m">
    try {
      init_script.delete();
      init_script.createNewFile();
      BufferedWriter init_script_writer = new BufferedWriter(new FileWriter(init_script));

      ArrayList<String> lines = new ArrayList<String>();

      //Declare the variables global BEFORE they are initialized, otherwise weird things happen with scope.
      lines.add("global " + CONST_TIMESTEPS + " "  + CONST_INIT_CONC + " " + CONST_NUM_ODES + " " +
              CONST_ODE_OPTS + " " + CONST_ODE_SOLUTION + " " + CONST_NOISE + " " + CONST_NUM_DATASETS + " " +
              CONST_NUM_PARAMS + " " + CONST_NUM_CONSTANTS + " " + CONST_COLORS);
      lines.add("format long;");
      lines.add(CONST_NUM_ODES + " = " + init_concentrations[0].length + ";");
      lines.add(CONST_NUM_DATASETS + " = " + init_concentrations.length + ";");
      lines.add(CONST_NUM_PARAMS + " = " + gfg.getNumParameters() + ";");
      lines.add(CONST_NUM_CONSTANTS + " = " + gfg.getNumZeroODEs() + ";");
      lines.add(CONST_NOISE + " = " + GAParameters.DATA_NOISE_PCT + ";");
      lines.add(CONST_COLORS + " = [[1 0 0] [0 1 0] [0 0 1]];");

      String set_init_conc = CONST_INIT_CONC + " = [";
      for (int i = 0; i < init_concentrations.length; ++i) {
        for(int j = 0; j < init_concentrations[i].length; ++j){
          set_init_conc += init_concentrations[i][j] + " ";
        }
      }
      set_init_conc += "];";

      lines.add(set_init_conc);
      //lines.add(OPTS_VAR + " = odeset();");
      lines.add(CONST_ODE_OPTS + " = odeset(\'NonNegative\', 1:" + CONST_NUM_ODES + ");");
      lines.add(CONST_TIMESTEPS + " = gen_t(" + GAParameters.T_MAX + ", " + GAParameters.T_SAMPLES + ", " + GAParameters.T_BIAS + ");");
      lines.add(CONST_ODE_SOLUTION + " = " + FUNC_NOISE + "(" + FUNC_EXEC_ODE + "(\'" + FUNC_INIT_ODE + "\'));");

      for (Iterator<String> it = lines.iterator(); it.hasNext();){
        init_script_writer.write(it.next());
        init_script_writer.newLine();
      }

      init_script_writer.close();
    }
    catch (IOException ioe) {
      GAMain.failWithError(ioe);
    }
    // </editor-fold>

    shutdown_comms = new ShutdownThread();
    Runtime.getRuntime().addShutdownHook(shutdown_comms);
    startMatlab();
  }

  // This function is identical to chromosomeToString, namely to ensure that any
  // changes to chromosomeToString don't affect this. This must always produce
  // a full set of ODEs.
  private String chromosomeToEquationSet(IChromosome a_subject){
    return ((GeneralFormGene) a_subject.getGene(0)).toString(true);
  }

  // <editor-fold defaultstate="collapsed" desc="MATLAB Interface Functions">
  private void startMatlab() {
    GAMain.statusMessage("Starting Matlab...", 2);
    try {
      matlab_process = Runtime.getRuntime().exec(CMD_INIT_MATLAB);
      shutdown_comms.setMatlabProcess(matlab_process);
    } catch (IOException ioe) {
      GAMain.failWithError(ioe);
    }

    GAMain.statusMessage("Attempting to run initialization, expect some retries while Matlab starts...", 2);
    // This makes the assumption that the initialization script won't hang Matlab.
    execute(SCRIPT_INITIALIZE, true);
  }

  private void killMatlab() {
    matlab_process.destroy();
  }

  private String execute(String exp) {
    return execute(exp, false);
  }

  private String execute(String exp, boolean retry) {
    GAMain.statusMessage(exp, 3);
    int tries = 0;
    MatlabExpression me = new MatlabExpression(exp);
    do {
      try {
        me.execute();
        // GAMain.statusMessage(me.getResult().toString());
        return me.getResult().toString();
      } catch (ConnectException ce) {
        if (!retry || ++tries == MAX_RETRIES) {
          GAMain.failWithError(ce);
        }
        try {
          Thread.sleep(RETRY_WAIT_MS);
        } catch (InterruptedException ie) {
          GAMain.failWithError(ie);
        }
        GAMain.statusMessage("Retrying Matlab connection...", 2);
      } catch (SocketTimeoutException ste) {
        GAMain.statusMessage("Matlab timed out, killing and restarting...", 2);
        killMatlab();
        startMatlab();
        return MATLAB_ERROR;
      } catch (SocketException se) {
        GAMain.statusMessage("Connection was reset, restarting Matlab and retrying command...", 2);
        killMatlab();
        startMatlab();
        return execute(exp, retry);
      } catch (EOFException eofe) {
        GAMain.statusMessage("Matlab encountered an EOF - potential communication error, retrying...", 2);
        return execute(exp, retry);
      } catch (StreamCorruptedException sce) {
        GAMain.statusMessage("eeoe (?) reading from stream - potential communication error, retrying...", 2);
        return execute(exp, retry);
      } catch (Exception e) {
        GAMain.failWithError(e);
      }
    } while (retry);

    assert (false) : "This shouldn't happen!";
    return "";
  }

  private void generateODEFile(String diff_eqs, String func_name, File f) {
    try {
      f.delete();
      f.createNewFile();
      BufferedWriter bw = new BufferedWriter(new FileWriter(f));
      bw.write("function " + VAR_ODE_PARAM + " = " + func_name + "(t, " + VAR_ODE_SOLUTION + ")");
      bw.newLine();
      bw.write(VAR_ODE_PARAM + " = zeros(size(" + VAR_ODE_SOLUTION + "));");
      bw.newLine();
      bw.write(diff_eqs);
      bw.newLine();
      bw.close();
    } catch (IOException ioe) {
      GAMain.failWithError(ioe);
    }
  }
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="DataGeneratingFitnessFunction Interface">
  public void generateTestData(IChromosome a_subject){
    generateTestData(chromosomeToEquationSet(a_subject));
  }

  public void generateTestData(String diff_eqs){
    File test_mfile = new File(FILE_PATH + FUNC_INIT_ODE + ".m");
    generateODEFile(diff_eqs, FUNC_INIT_ODE, test_mfile);
    execute(SCRIPT_INITIALIZE + ";");
    answer_t_set = answer_var_set = true;
  }

  public void setTestData(double[][][] data, double[] delta_ts){
    GAMain.failWithError(new UnsupportedOperationException("MATLAB can generate its own test data."));
  }

  public void update(int generation, Population pop){
    return;
  }
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="JGAP Interface">
  public double evaluate(IChromosome a_subject) {
    GeneralFormGene gfg = (GeneralFormGene) a_subject.getGene(0);
    if (gfg.getFitness() == FitnessFunction.NO_FITNESS_VALUE) {
      if (!answer_t_set || !answer_var_set) {
        String error = "";
        if (!answer_t_set) {
          error += "No reference t-values have been set. ";
        }
        if (!answer_var_set) {
          error += "No reference data values have been set.";
        }
        throw new IllegalStateException(error);
      }

      GAMain.statusMessage("Generating new mfile for member...", 3);
      generateODEFile(chromosomeToEquationSet(a_subject), FUNC_ODE, mfile);

      GAMain.statusMessage("Clearing old names...", 3);
      execute("clear " + FUNC_ODE);

      GAMain.statusMessage("Solving ODE...", 3);
      String result = execute(ode_command);

      if (result.equals(MATLAB_ERROR)) {
        GAMain.statusMessage("Execute errored, using NaN.", 3);
        result = "NaN";
      }
      else {
        GAMain.statusMessage("Calculating error...", 3);
        result = execute(error_command);
      }

      GAMain.statusMessage("Parsing out error from return string \"" + result +"\"...", 3);
      double error = extractErrorValue(result);

      GAMain.statusMessage("Error: " + error, 3);
      gfg.setFitness(error);
      return error;

    } else {
      GAMain.statusMessage("Fitness already exists!", 3);
      return gfg.getFitness();
    }
  }
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="JGAP Interface Helper Functions">
  private static double extractErrorValue(String s) throws IllegalArgumentException {
    Matcher m = MATCH_ERROR_ASSIGN.matcher(s);
    if (m.find()) {
      m = MATCH_NUMBER.matcher(m.group());
      m.find();
      if (!m.group().equals("Inf") && !m.group().equals("NaN")) {
        return Double.valueOf(m.group());
      }
      return Double.MAX_VALUE;
    }
    throw new IllegalArgumentException("\'" + s + "\' does not contain a number.");
  }
  // </editor-fold>

  public String toString(){
    return "Fitness computed using MATLAB.";
  }
}
