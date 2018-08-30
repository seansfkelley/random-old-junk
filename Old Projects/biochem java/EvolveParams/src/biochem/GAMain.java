package biochem;

import java.util.*;
import java.io.*;
import org.jgap.*;
import org.jgap.impl.*;
import org.jgap.event.*;

class GAMain{
  private static int lineno = 1, generation;

  private static long start_time;

  private static DataBasedFitnessFunction fit_func;
  private static Genotype                 population = null;
  
  public static void main(String[] args) throws Exception{
    if (!GAParameters.OUTPUT_FILE.equals("")){
      System.setOut(new PrintStream(new BufferedOutputStream(new FileOutputStream(GAParameters.OUTPUT_FILE))));
    }

    // <editor-fold defaultstate="collapsed" desc="Instantiate Configuration/Setup Initial Concentrations">
    Configuration config = new Configuration();

    // Change static text data, too!

    // ode2
    // double[][] init_concs = {{1, 2.5, 2}};

    // ode3
    // double[][] init_concs = {{1, 1, 2}, {1, 1, 1.5}, {1, 1, .75}};

    // ode2-13
    // double[][] init_concs = {{2, .1, .5, 1}, {.5, 2.5, .5, 1}, {1.5, 2, 1, .5}};

    // ode3-28
    double[][] init_concs = {{4, 2, 6, 10, 5, 1, 1, 1, 1, 1},
                             {2, 2.5, 3, 5, 6, 5.5, 0.5, 5.5, 0.5, 5.5}};
                             // {3, 4, 5, 1, 1, 10, 10, 10, 10, 10}};
    // </editor-fold>

    // <editor-fold defaultstate="collapsed" desc="Generate Sample Genes for Chromosome">
    SparseMultiMatrix alpha = new SparseMultiMatrix(4, GAParameters.ALPHA_DENOM),
                      beta =  new SparseMultiMatrix(4, GAParameters.BETA_DENOM),
                      gamma = new SparseMultiMatrix(3, GAParameters.GAMMA_DENOM),
                      k =     new SparseMultiMatrix(2, GAParameters.K_DENOM);

    // <editor-fold defaultstate="collapsed" desc="ode2-8">
//    gamma.put(1, 0, 0, 0);
//    gamma.put(1, 0, 1, 2);
//    gamma.put(1, 1, 0, 1);
//    gamma.put(1, 1, 1, 2);
//
//    k.put(-1, 0, 0);
//    k.put( 1, 0, 1);
//    k.put(-2, 1, 0);
//    k.put( 2, 1, 1);
    // </editor-fold>

    // <editor-fold defaultstate="collapsed" desc="ode3-28">

    alpha.put(0.45625, 1, 0, 0, 1);
    alpha.put(4.29,    2, 0, 0, 2);

    alpha.put(1.05, 0, 1, 0, 1);
    alpha.put(4.29, 1, 1, 0, 2);

    beta.put(1, 1, 0, 0, 1);
    beta.put(1, 2, 0, 0, 2);

    beta.put(1, 0, 1, 0, 1);
    beta.put(1, 1, 1, 0, 2);

    gamma.put(0.63,   0, 0, 3);
    gamma.put(1,      0, 0, 5);
    gamma.put(0.75,   1, 0, 0);
    gamma.put(0.5125, 1, 0, 4);
    gamma.put(0.375,  1, 0, 6);
    gamma.put(0.625,  1, 0, 9);
    gamma.put(4.65,   2, 0, 1);
    gamma.put(1,      2, 0, 7);

    gamma.put(2, 0, 1, 0);
    gamma.put(1, 0, 1, 6);
    gamma.put(4.65, 1, 1, 1);
    gamma.put(1, 1, 1, 7);
    gamma.put(0.3, 2, 1, 2);
    gamma.put(1, 2, 1, 8);

    k.put( 0.0017581, 0, 0);
    k.put(-1.44890,   0, 1);
    k.put( 0.0604276, 1, 0);
    k.put(-0.0001934, 1, 1);
    k.put( 0.0001934, 2, 0);
    k.put(-0.0346570, 2, 1);

    // </editor-fold>

    // <editor-fold defaultstate="collapsed" desc="ode2-13">
    
//    SparseMultiMatrix alpha = new SparseMultiMatrix(4),
//                      beta =  new SparseMultiMatrix(4),
//                      gamma = new SparseMultiMatrix(3),
//                      k =     new SparseMultiMatrix(2);
//    alpha.put(1 * GAParameters.ALPHA_DENOM, 0, 1, 0, 2 );
//    alpha.put(1 * GAParameters.ALPHA_DENOM, 1, 0, 0, 2);
//
//    beta.put(1 * GAParameters.BETA_DENOM, 0, 1, 0, 2);
//    beta.put(1 * GAParameters.BETA_DENOM, 1, 0, 0, 2);
//
//    gamma.put(1 * GAParameters.GAMMA_DENOM, 0, 0, 1);
//    gamma.put((int) (0.5 * GAParameters.GAMMA_DENOM), 0, 1, 0);
//    gamma.put((int) (0.1 * GAParameters.GAMMA_DENOM), 1, 0, 0);
//    gamma.put((int) (0.5 * GAParameters.GAMMA_DENOM), 1, 0, 3);
//    gamma.put(1 * GAParameters.GAMMA_DENOM, 1, 1, 1);
//
//    k.put(2 * GAParameters.K_DENOM, 0, 0);
//    k.put((int) (-1.2 * GAParameters.K_DENOM), 0, 1);
//    k.put(2 * GAParameters.K_DENOM, 1, 0);
//    k.put(-2 * GAParameters.K_DENOM, 1, 1);
    
    // </editor-fold>

    // <editor-fold defaultstate="collapsed" desc="ode3">
//    SparseMultiMatrix alpha = new SparseMultiMatrix(4),
//                  beta =  new SparseMultiMatrix(4),
//                  gamma = new SparseMultiMatrix(3),
//                  k =     new SparseMultiMatrix(2);
//    alpha.put(new int[]{0, 0, 0, 1}, 2 * GAParameters.ALPHA_DENOM);
//
//    beta.put(new int[]{0, 0, 0, 1}, 1 * GAParameters.BETA_DENOM);
//
//    gamma.put(new int[]{0, 0, 2}, 1 * GAParameters.GAMMA_DENOM);
//    gamma.put(new int[]{0, 1, 0}, (int) (0.5 * GAParameters.GAMMA_DENOM));
//    gamma.put(new int[]{0, 1, 1}, 1 * GAParameters.GAMMA_DENOM);
//    gamma.put(new int[]{1, 0, 0}, (int) (0.5 * GAParameters.GAMMA_DENOM));
//    gamma.put(new int[]{1, 0, 1}, 1 * GAParameters.GAMMA_DENOM);
//    gamma.put(new int[]{1, 1, 1}, (int) (0.5 * GAParameters.GAMMA_DENOM));
//
//    k.put(new int[]{0, 0}, 1 * GAParameters.K_DENOM);
//    k.put(new int[]{0, 1}, -1 * GAParameters.K_DENOM);
//    k.put(new int[]{1, 0}, 1 * GAParameters.K_DENOM);
//    k.put(new int[]{1, 1}, -1 * GAParameters.K_DENOM);
    // </editor-fold>

    GeneralFormGene[] sampleGenes = new GeneralFormGene[1];
    sampleGenes[0] = new GeneralFormGene(config, init_concs[0].length);
    sampleGenes[0].setAllele(new SparseMultiMatrix[]{alpha, beta, gamma, k});

    Chromosome sampleChromosome = new Chromosome(config, sampleGenes);
    config.setSampleChromosome(sampleChromosome);
    // </editor-fold>

    // <editor-fold defaultstate="collapsed" desc="Setup Configuration">
    // fit_func = new GeneralFormMatlabFitness(init_concs);
    // fit_func = new GeneralFormFitness(init_concs);
    fit_func = new GeneralFormDualFitness(init_concs, sampleGenes[0]);

    GAParameters.update();

    // Copied and modified as appropriate from the code in DefaultConfiguration.
    config.setBreeder(new GABreeder());
    config.setRandomGenerator(new StockRandomGenerator());
    config.setEventManager(new EventManager());
    // BestChromosomesSelector bestChromsSelector = new BestChromosomesSelector(config, GAParameters.MEMBER_KEEP_RATE);
    // bestChromsSelector.setDoubletteChromosomesAllowed(false);
    // config.addNaturalSelector(bestChromsSelector, false);
    config.addNaturalSelector(new WeightedSelector(config, GAParameters.MEMBER_KEEP_RATE, GAParameters.FITNESS_SELECTION_BIAS, (GeneralFormDualFitness) fit_func), false);
    config.setMinimumPopSizePercent(100);

    config.setSelectFromPrevGen(1.0);
    config.setKeepPopulationSizeConstant(true);
    config.setFitnessFunction(fit_func);
    config.setFitnessEvaluator(new DefectRateEvaluator(fit_func));
    config.setChromosomePool(new ChromosomePool());
    config.addGeneticOperator(new GeneralFormCrossover(config, GAParameters.CROSSOVER_RATE, true));
    config.addGeneticOperator(new GeneralFormMutation(config, GAParameters.MUTATION_RATE, true));//, GAParameters.MUTATION_SA_RATE));
    config.addGeneticOperator(new GeneralFormSmallMutation(config, GAParameters.MUTATION_MAX_SMALL_CHANGE));//, GAParameters.MUTATION_SMALL_CHANGE_REPETITIONS));

    // I don't trust JGAP's fitness caching. It isn't clear how it works or what
    // is required to make it work. It's only ever given me trouble by assigning
    // fitnesses in the wrong places (presumably because whatever was required
    // to differentiate members wasn't correctly implemented, if at all). For
    // these reasons, I used my own workaround -- first a String -> Integer hash
    // in the fitness function, but after that got slow and unwieldly I switched
    // to holding the fitness in each GeneralFormGene.
    config.setAlwaysCaculateFitness(true);
    config.setPopulationSize(GAParameters.POP_SIZE);

    // Allow both crossover and mutation for all members.
    config.getJGAPFactory().setGeneticOperatorConstraint(null);
    // </editor-fold>

    // <editor-fold defaultstate="collapsed" desc="Setup Test Data">
    // For GeneralFormFitness.
    // fit_func.setTestData(Data.data_1, Data.data_1_dt);

    // For GeneralFormMatlabFitness.
    // fit_func.generateTestData(sampleChromosome);

    // For GeneralFormDualFitness.
    fit_func.generateTestData(sampleChromosome);
    fit_func.setTestData(Data_ODE3_28.all_data, Data_ODE3_28.dt);
    // </editor-fold>
    
    // <editor-fold defaultstate="collapsed" desc="Output Evolution Parameters">
    GAParameters.printInformation();
    GAMain.statusMessage("Evolving " + init_concs[0].length + " equations using " + init_concs.length + " datasets", 1);
    for (Object o : config.getGeneticOperators()){
      GAMain.statusMessage(o.toString(), 1);
    }
    GAMain.statusMessage(fit_func.toString(), 1);
    GAMain.statusMessage("Original ODE System:\n" + sampleGenes[0].toString(true), 1);
    // </editor-fold>

    // <editor-fold defaultstate="collapsed" desc="Evolution">
    start_time = System.currentTimeMillis();
    try {
      population = Genotype.randomInitialGenotype(config);

      for (generation = 0; generation < GAParameters.GENERATIONS; generation++) {
        if (!uniqueChromosomes(population.getPopulation())) {
          GAMain.failWithError(new RuntimeException("Invalid state in generation " + generation));
        }
        // System.err.println("Beginning generation " + generation + " (t=" + Main.timeElapsed() + ")");
        GAMain.statusMessage("Beginning generation " + generation + " (t=" + GAMain.timeElapsed() + ")", 1);
        population.evolve();
        printPopulation(false, false, true);
        fit_func.update(generation, population.getPopulation());
      }

      printPopulation(true, GAParameters.PRINT_BEST_RESULT_ONLY, false);
      OperatorTallies.printTallies();
    } catch (Exception e) {
      GAMain.failWithError(e);
    }

    GAMain.statusMessage("Total evolution time: " + GAMain.timeElapsed(), 0);
    // </editor-fold>
  }

  // <editor-fold defaultstate="collapsed" desc="Helper Functions for GAMain">
  public static boolean uniqueChromosomes(Population a_pop) {
    // Lifted straight out of one of the examples.
    IChromosome c1, c2;
    for (int i = 0; i < a_pop.size() - 1; i++) {
      c1 = a_pop.getChromosome(i);
      for (int j = i + 1; j < a_pop.size(); j++) {
        c2 = a_pop.getChromosome(j);
        if (c1.equals(c2)) {
          return false;
        }
      }
    }
    return true;
  }

  public static void statusMessage(String status) {
    GAMain.statusMessage(status, 2);
  }

  public static void statusMessage(String status, int priority) {
    if (GAParameters.PRINT_STATUSES >= priority) {
      System.out.println((GAParameters.USE_LINE_NUMBERS ? lineno + " " : "") + status);
      lineno++;
      System.out.flush();
    }
  }

  public static String timeElapsed() {
    long end_time = System.currentTimeMillis();
    long seconds = (end_time - start_time) / 1000;
    int minutes = (int) (seconds / 60);
    seconds %= 60;

    return minutes + ":" + (seconds < 10 ? "0" : "") +
            seconds + " (" + (end_time - start_time) + "ms)";
  }

  public static void failWithError(Exception e) {
    printPopulation(false);
    e.printStackTrace();
    GAMain.statusMessage("Failure at t=" + GAMain.timeElapsed(), 0);
    System.exit(1);
  }

  public static IChromosome printPopulation() {
    return printPopulation(true);
  }

  public static IChromosome printPopulation(boolean sorted){
    return printPopulation(sorted, false);
  }

  public static IChromosome printPopulation(boolean sorted, boolean onlyFittest){
    return printPopulation(sorted, onlyFittest, false);
  }

  public static IChromosome printPopulation(boolean sorted, boolean onlyFittest, boolean onlyFitness){
    if (population == null){
      statusMessage("Population is not initialized.\n", 0);
      return null;
    }

    ArrayList<IChromosome> members = new ArrayList<IChromosome>(population.getPopulation().size());
    for (Iterator i = population.getPopulation().iterator(); i.hasNext();) {
      members.add((IChromosome) i.next());
    }

    if (sorted){
      // The comparator, of course, operates on fitnesses. Thus, it should not
      // be used if the algorithm terminated abnormally, since fitness potentially
      // calls Matlab, and Matlab is most likely the reason for the early
      // termination. Lots of StackOverflowErrors died to bring us this
      // information.
      Comparator icc = new IChromosomeComparator();
      Collections.sort(members, icc);
      Collections.reverse(members);
    }

    GeneralFormGene gfg;

    if (onlyFittest){
      IChromosome ic = members.get(members.size() - 1);
      statusMessage(ic.toString() + ", Age:" + ic.getAge(), 0);
      gfg = (GeneralFormGene) ic.getGene(0);
      statusMessage("\n" + gfg.toString(true) + "\n", 0);
      return members.get(members.size() - 1);
    }

    for (int i = 0; i < members.size(); ++i){
      IChromosome ic = members.get(i);
      if (onlyFitness){
        statusMessage(generation + " " + ic.getFitnessValue(), 0);
      }
      else{
        statusMessage(ic.toString() + ", Age:" + ic.getAge(), 0);
        gfg = (GeneralFormGene) ic.getGene(0);
        statusMessage("\n" + gfg.toString(true) + "\n", 0);
      }
    }

    return members.get(members.size() - 1);
  }
  // </editor-fold>
}