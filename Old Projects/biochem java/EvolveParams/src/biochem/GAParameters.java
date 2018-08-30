package biochem;

public class GAParameters{
  // <editor-fold defaultstate="collapsed" desc="Output Parameters">
  // Leave as am empty string for stdout.
  // public static final String OUTPUT_FILE = "";
  public static final String OUTPUT_FILE = "/Users/sk/Documents/Programming/Biochem Data/Fitness Plots/output.txt";

  // This variable allows toggling the amount of information output during the
  // GA's run.
  public static final int PRINT_STATUSES = 1;
  // 0: Print nothing except the answers at the end.
  // 1: Print the parameters for the run and notices for each generation.
  // 2: Describe the general course of each step the GA takes.
  // 3: Print almost everything that's happening.

  // Only applies to the final printing of the population.
  public static final boolean PRINT_BEST_RESULT_ONLY = false;
  
  // For GAMain.statusMessage().
  public static final boolean USE_LINE_NUMBERS = true;
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="General GA Parameters">
  public static final int GENERATIONS = 200, POP_SIZE = 200;
  // What percentage of members are retained from a generation for the next
  // generation.
  public static final double MEMBER_KEEP_RATE = 0.20;

  // The average fitness of the fittest MEMBER_KEEP_RATE portion of the population
  // must change less than this percentage before fitness is swiched over to MATLAB.
  public static final double FITNESS_SWITCH_THRESHOLD = 0.001; // 0.0005;

  // How many generations until fitness is switched. Set to zero to use the
  // threshold value instead.
  public static final int FITNESS_SWITCH_GENERATIONS = 100;

  // How biased towards the higher end of the population the WeightedSelector
  // will be. 1 is a small but noticeable amount, 4 is about as high as you would
  // want to go.
  public static final double FITNESS_SELECTION_BIAS = 2.5;
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="Data Generation Parameters">
  public static final double T_MAX = 10, T_BIAS = 1.667, DATA_NOISE_PCT = 0.00;
  public static final int T_SAMPLES = 350;
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="Mutation Parameters">
  // The different types of mutation that the GeneralFormGene's applyMutation
  // knows how to do.
  // Relative: mutate a percentage of the current value (default).
  // Absolute: mutate an absolute amount away from the current value.
  // Random: replace the current value with a totally random one.
  public static enum MutationType {RELATIVE, ABSOLUTE, RANDOM};

  // Mutation only supports three core types (listed above), but their input
  // values can be preprocessed to produce a variety of different /conceptual/
  // mutation types, listed here. These are for use in the tallies, ONLY.
  public static enum MutationTypeNominal {ANNEAL, RANDOM, RELATIVE_ERROR_BASED, RELATIVE_RANDOM};

  public static double MUTATION_RATE = 0.4;

  // Of the members selected for mutation, how many are going to be mutated
  // absolutely randomly.
  public static double MUTATION_RANDOM_RATE = 0.25;

  // The percentage of members already selected for mutation that will have
  // quick simulated annealing done instead of a standard mutation.
  public static final double MUTATION_SA_RATE = 0.10;

  // The worst fit individual will be mutated by this amount. 1 = 100% of the
  // current value. Note that most of the population tends to fall below 50%
  // of the worst fit's fitness.
  // "DFR" = Dynamic Fitness Range
  public static final double MUTATION_DFR_EXTENSION = 0.5;

  // The minimum mutation amount.
  public static final double MUTATION_BASELINE = 0.25,
                             MUTATION_RANGE = 1 - MUTATION_BASELINE;

  // The maximum allowed change for a small random mutation.
  public static final int MUTATION_MAX_SMALL_CHANGE = 6;

  // How many small random mutations are allowed to happen to a single member
  // simultaneously.
  public static final int MUTATION_SMALL_CHANGE_REPETITIONS = 4;
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="Crossover Parameters">
  public static double CROSSOVER_RATE = 0.6;

  // 1 = no effect; 2 is recommended. Higher means more bad-fitness members will
  // be lumped together with a rate = 1, but there will be better resolution for
  // the members with less bad fitnesses.
  public static double CROSSOVER_DFR_EXTENSION = 1.25;

  // The allowable types of crossover, listing in increasing order of severity.
  public static enum CrossoverType {DENOM_TERM, DENOM, NUMER, DENOM_K, NUMER_K, TERM, TERM_K, EQUATION};
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="Parameter Ranges">
  // The following fice groups are split among actual input parameters to the GA
  // and composite values designed for readability/understandability.
  // Denominators: Dictate the precision of each parameter type -- this is
  // synonymous with the number of steps between integers for the appropriate
  // parameter type.
  public static int ALPHA_DENOM = 10,
                    BETA_DENOM = 100,
                    GAMMA_DENOM = 10,
                    K_DENOM = 10000;

  // Mins/Maxes (Reference versions): The true allowable range of each parameter.
  // These should never be used outside this class except to change the range
  // of values at runtime. All other computations should be done using the
  // appropriate *_MIN variable.
  // Important note: the values for beta have a special exception due to their
  // nature as denominators. If the range includes zero, the program will error,
  // unless either endpoint is exactly zero, in which case the denominator-expanded
  // value corresopnding to it will be set to ±1, as appropriate.
  public static double ALPHA_MIN_REF = -2, ALPHA_MAX_REF = 2,
                       BETA_MIN_REF =   0, BETA_MAX_REF = 10,
                       GAMMA_MIN_REF =  0, GAMMA_MAX_REF = 2,
                       K_MIN_REF =    -10, K_MAX_REF =    10;

  // These next three are the composite values -- just to make reading and
  // writing the code easier.
  // Denominators (Double versions): The parameters are all integers, but the
  // values they compute are doubles and casting each of the denominators to
  // different types almost everywhere they're used is silly.
  public static double ALPHA_DENOM_D, BETA_DENOM_D, GAMMA_DENOM_D, K_DENOM_D;

  // Mins/Maxes: The denominator-expanded versions. These are the ones that are
  // used most often in the code.
  public static int ALPHA_MIN, ALPHA_MAX,
                    BETA_MIN,  BETA_MAX,
                    GAMMA_MIN, GAMMA_MAX,
                    K_MIN,     K_MAX;

  // Arrays: Conversion between an integer and a value. Some places in the code
  // benefit most from using an index rather than an enum type or similar.
  public static int[] MINS, MAXS;
  public static double[] DENOMS_D;
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="MATLAB Strings">
  public static final String MATLAB_VAR_ODE_SOLUTION = "X",
                             MATLAB_VAR_ODE_PARAM = "d" + MATLAB_VAR_ODE_SOLUTION + "dt";
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="Utility Functions">
  // This function must be called at least during the lifetime of the program to
  // initialize the composite types.
  public static void update() {
    assert (ALPHA_DENOM * BETA_DENOM * GAMMA_DENOM * K_DENOM != 0) :
            "A denominator in GAParameters is zero.";

    ALPHA_DENOM_D = ALPHA_DENOM;
    BETA_DENOM_D =  BETA_DENOM;
    GAMMA_DENOM_D = GAMMA_DENOM;
    K_DENOM_D =     K_DENOM;

    ALPHA_MIN = (int) (ALPHA_MIN_REF * ALPHA_DENOM);
    ALPHA_MAX = (int) (ALPHA_MAX_REF * ALPHA_DENOM);

    // < 0 if they differ in sign.
    if (BETA_MIN_REF * BETA_MAX_REF < 0) {
      GAMain.failWithError(new Exception("Range for beta includes zero."));
    } else if (BETA_MIN_REF * BETA_MAX_REF == 0) {
      if (BETA_MIN_REF == 0) {
        BETA_MIN = 1;
        BETA_MAX = (int) (BETA_MAX_REF * BETA_DENOM);
      } else {
        BETA_MIN = (int) (BETA_MIN_REF * BETA_DENOM);
        BETA_MAX = -1;
      }
    } else {
      BETA_MIN = (int) (BETA_MIN_REF * BETA_DENOM);
      BETA_MAX = (int) (BETA_MAX_REF * BETA_DENOM);
    }

    GAMMA_MIN = (int) (GAMMA_MIN_REF * GAMMA_DENOM);
    GAMMA_MAX = (int) (GAMMA_MAX_REF * GAMMA_DENOM);

    K_MIN = (int) (K_MIN_REF * K_DENOM);
    K_MAX = (int) (K_MAX_REF * K_DENOM);

    MINS = new int[]{ALPHA_MIN, BETA_MIN, GAMMA_MIN, K_MIN};
    MAXS = new int[]{ALPHA_MAX, BETA_MAX, GAMMA_MAX, K_MAX};
    DENOMS_D = new double[]{ALPHA_DENOM_D, BETA_DENOM_D, GAMMA_DENOM_D, K_DENOM_D};
  }

  public static void printInformation() {
    GAMain.statusMessage("Generations: " + GENERATIONS + "; Pop size: " + POP_SIZE + "; Keep Rate: " + (MEMBER_KEEP_RATE * 100) + "%", 1);
    GAMain.statusMessage("T max: " + T_MAX + "; T samples: " + T_SAMPLES + " T bias: " +
            T_BIAS + " Noise: ±" + (DATA_NOISE_PCT * 100) + "%", 1);

    GAMain.statusMessage("alpha: [" + ALPHA_MIN_REF + ", " +
            ALPHA_MAX_REF + "] @ 1/" + ALPHA_DENOM, 1);
    GAMain.statusMessage("beta:  [" + BETA_MIN_REF + ", " +
            BETA_MAX_REF + "] @ 1/" + BETA_DENOM, 1);
    GAMain.statusMessage("gamma: [" + GAMMA_MIN_REF + ", " +
            GAMMA_MAX_REF + "] @ 1/" + GAMMA_DENOM, 1);
    GAMain.statusMessage("k:     [" + K_MIN_REF + ", " +
            K_MAX_REF + "] @ 1/" + K_DENOM, 1);
  }
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="Parameter Changes">
  // These will never be seen outside of this code, but this function should be
  // called at each generation.
//  private static final int K_DENOM_START = K_DENOM, K_DENOM_END = 10000,
//                           BETA_DENOM_START = BETA_DENOM
//
//  public static void changeParameters(int generation) {
//
//  }
  // </editor-fold>
}