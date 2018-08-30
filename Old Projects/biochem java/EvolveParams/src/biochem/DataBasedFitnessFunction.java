package biochem;

import org.jgap.*;

public abstract class DataBasedFitnessFunction extends FitnessFunction{
  public abstract void generateTestData(IChromosome a_subject);
  public abstract void setTestData(double[][][] data, double[] delta_ts);
  public abstract void update(int generation, Population pop);
}
