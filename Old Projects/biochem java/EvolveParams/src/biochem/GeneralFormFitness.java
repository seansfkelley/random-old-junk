package biochem;

import org.jgap.*;

public class GeneralFormFitness extends DataBasedFitnessFunction{

  private boolean has_data, data_given;
  private double[] delta_t; // indexed by timestep
  private double[][] init_concs; // indexed by dataset, metabolite
  private double[][][] all_datasets; // indexed by dataset, timestep, metabolite

  public GeneralFormFitness(double[][] init_concentrations){
    init_concs = init_concentrations;
    has_data = false;
  }

  // <editor-fold defaultstate="collapsed" desc="DataGeneratingFitnessFunction Interface">
  public void generateTestData(IChromosome a_subject) {
    GeneralFormGene gfg = (GeneralFormGene) a_subject.getGene(0);

    generateDeltaT();
    all_datasets = new double[init_concs.length][delta_t.length + 1][init_concs[0].length];

    double[] temp_array;

    for (int dataset = 0; dataset < init_concs.length; ++dataset) {
      all_datasets[dataset][0] = init_concs[dataset];
      for (int t = 1; t < delta_t.length + 1; ++t) {
        temp_array = gfg.evaluate(all_datasets[dataset][t - 1]);
        for (int m = 0; m < temp_array.length; ++m) {
          // Use the Euler or RK4 functions here.
          all_datasets[dataset][t][m] = all_datasets[dataset][t - 1][m] + temp_array[m] * delta_t[t - 1];
          // System.out.print(all_datasets[dataset][t][m] + " ");
        }
        // System.out.println();
      }
    }

    has_data = true;
    data_given = false;
  }

  public void setTestData(double[][][] data, double[] delta_ts) {
    all_datasets = data;
    delta_t = delta_ts;
    has_data = true;
    data_given = true;
  }

  public void update(int generation, Population pop){
    return;
  }
  // </editor-fold>
  
  // <editor-fold defaultstate="collapsed" desc="DataGeneratingFitnessFunction Interface Helper Functions">
  private void generateDeltaT() {
    double[] absolute_t = new double[GAParameters.T_SAMPLES];
    for (int i = 1; i <= GAParameters.T_SAMPLES; ++i) {
      absolute_t[i - 1] = GAParameters.T_MAX * ((Math.exp((i * GAParameters.T_BIAS) / GAParameters.T_SAMPLES) - 1) / (Math.exp(GAParameters.T_BIAS) - 1));
    }

    delta_t = new double[GAParameters.T_SAMPLES - 1];
    for (int i = 1; i < GAParameters.T_SAMPLES; ++i) {
      delta_t[i - 1] = absolute_t[i] - absolute_t[i - 1];
    }
  }
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="JGAP Interface">
  public double evaluate(IChromosome a_subject) {
    if (!has_data) {
      throw new IllegalStateException("Test data not yet generated.");
    }
    GeneralFormGene gfg = (GeneralFormGene) a_subject.getGene(0);
    if (gfg.getFitness() == FitnessFunction.NO_FITNESS_VALUE){
      double fitness = 0;
      for (int i = 0; i < all_datasets.length; ++i) {
        fitness += calculateErrorForDataset(gfg, all_datasets[i]);
      }
      // Average error across all datasets.
      fitness /= all_datasets.length;

      gfg.setFitness(fitness);
      return fitness;
    }
    else{
      GAMain.statusMessage("Fitness already exists!", 3);
      return gfg.getFitness();
    }
  }
  // </editor-fold>

  // <editor-fold defaultstate="collapsed" desc="JGAP Interface Helper Functions + Integration">
  private double calculateErrorForDataset(GeneralFormGene gfg, double[][] data) {
    double error = 0;
    double[] concs;
    for (int t = 1; t < data.length; ++t) {
      concs = EulerIntegrationStep(gfg, data[t - 1], delta_t[t - 1]);
      for (int m = 0; m < concs.length; ++m) {
        error += Math.pow((data[t][m] - concs[m]) / data[t][m], 2);
      }
    }
    if (Double.isNaN(error)){
      error = Double.MAX_VALUE;
    }
    // This divides by the number of timesteps, but the average error is still
    // the /sum/ of average errors for each of the metabolites.
    return error / delta_t.length;
  }

  private double[] EulerIntegrationStep(GeneralFormGene gfg, double[] concs, double dt) {
    double[] new_concs = gfg.evaluate(concs);
    for (int i = 0; i < new_concs.length; ++i) {
      new_concs[i] = concs[i] + new_concs[i] * dt;
    }
    return new_concs;
  }

  private double[] MidpointIntegrationStep(GeneralFormGene gfg, double[] concs, double dt){
    // Find midpoint.
    double[] new_concs = gfg.evaluate(concs);
    for (int i = 0; i < new_concs.length; ++i) {
      new_concs[i] = concs[i] + new_concs[i] * dt / 2;
    }
    // Perform Euler integration with this new estimate, starting from the
    // original starting point.
    new_concs = gfg.evaluate(new_concs);
    for (int i = 0; i < new_concs.length; ++i) {
      new_concs[i] = concs[i] + new_concs[i] * dt;
    }
    return new_concs;
  }

  // This functions appears to work, but has not been thoroughly tested. Due to
  // the nature of these equations, RK4 will yield NaN oftentimes because the
  // derivative at an ill-defined point is often taken (i.e. the derivative of
  // a point which has negative concentrations or other impossible scenarios,
  // because the equations are badly fit). Euler doesn't suffer from this, as it
  // does a single step. A negative concentration will result in a bad error for
  // that point and nothing more. It's also less accurate.
  private double[] RK4IntegrationStep(GeneralFormGene gfg, double[] concs, double dt) {
    int num_metabolites = concs.length;
    double[] new_concs, k1, k2, k3, k4;

    k1 = gfg.evaluate(concs);

    k2 = new double[num_metabolites];
    for (int i = 0; i < num_metabolites; ++i) {
      k2[i] = concs[i] + k1[i] * dt * 0.5;
    }
    k2 = gfg.evaluate(k2);

    k3 = new double[num_metabolites];
    for (int i = 0; i < num_metabolites; ++i) {
      k3[i] = concs[i] + k2[i] * dt * 0.5;
    }
    k3 = gfg.evaluate(k3);

    k4 = new double[num_metabolites];
    for (int i = 0; i < num_metabolites; ++i) {
      k4[i] = concs[i] * k3[i] * dt;
    }
    k4 = gfg.evaluate(k4);

    new_concs = new double[num_metabolites];
    for (int i = 0; i < num_metabolites; ++i) {
      new_concs[i] = concs[i] + ((1.0 / 6.0) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])) * dt;
    }

    return new_concs;
  }
  // </editor-fold>

  public String toString(){
    String s = "Fitness computed using Euler integration.";
    if (data_given){
      s += "\nUsing static data for fitness. Ensure dimensions of data are correct.";
    }
    return s;
  }
}
