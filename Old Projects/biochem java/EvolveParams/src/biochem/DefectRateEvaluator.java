package biochem;

import org.jgap.*;

public class DefectRateEvaluator implements FitnessEvaluator{
  private FitnessFunction ff;
  
  public DefectRateEvaluator(FitnessFunction fit){
    ff = fit;
  }
  
  public boolean isFitter(double a_fitness_value1, double a_fitness_value2){
    return a_fitness_value1 < a_fitness_value2;
  }
  
  public boolean isFitter(IChromosome a_chrom1, IChromosome a_chrom2){
    return isFitter(ff.getFitnessValue(a_chrom1), ff.getFitnessValue(a_chrom2));
  }
}