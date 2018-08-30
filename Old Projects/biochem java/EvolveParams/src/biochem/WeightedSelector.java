package biochem;

import org.jgap.*;
import java.util.*;

public class WeightedSelector extends NaturalSelector{
  private Population chromosomes;
  private FitnessValueComparator fitnessComparator;
  private GeneralFormDualFitness dualFitness;
  private double pct, bias;

  public WeightedSelector(Configuration config, double percentage, double selectionBias) throws InvalidConfigurationException{
    super(config);
    chromosomes = new Population(config);
    fitnessComparator = new FitnessValueComparator();
    pct = percentage;
    bias = selectionBias;
    dualFitness = null;
  }

  public WeightedSelector(Configuration config, double percentage, double selectionBias, GeneralFormDualFitness GFDualFitness) throws InvalidConfigurationException{
    super(config);
    chromosomes = new Population(config);
    fitnessComparator = new FitnessValueComparator();
    pct = percentage;
    bias = selectionBias;
    dualFitness = GFDualFitness;
  }

  @Override
  protected void add(IChromosome a_chromosomeToAdd) {
    if (chromosomes.getChromosomes().contains(a_chromosomeToAdd)) {
      return;
    }
    a_chromosomeToAdd.setIsSelectedForNextGeneration(false);
    chromosomes.addChromosome(a_chromosomeToAdd);
  }

  public void empty() {
    chromosomes.getChromosomes().clear();
  }

  public boolean returnsUniqueChromosomes() {
    return true;
  }

  public void select(int howMany, Population fromPop, Population toPop) {
    if (fromPop != null) {
      int popSize = fromPop.size();
      for (int i = 0; i < popSize; i++) {
            add(fromPop.getChromosome(i));
      }
    }

    int popSize = chromosomes.size();

    /*
    if (dualFitness != null && dualFitness.usingMatlab()){

      // Get the chromosomes in the right order.
      for (int i = 0; i < popSize; ++i){
        dualFitness.evaluateBuiltin(chromosomes.getChromosome(i));
      }
      Collections.sort(chromosomes.getChromosomes(), fitnessComparator);

      // Reset all the fitnesses, since we don't want to use the builtin value.
      for (int i = 0; i < popSize; ++i){
        ((GeneralFormGene) chromosomes.getChromosome(i).getGene(0)).setFitness(FitnessFunction.NO_FITNESS_VALUE);
      }

      // Binary search to find the worst one that Matlab can grade.
      int pos = popSize / 2, jump = popSize / 2;
      while (jump != 0){
        // jump is changed at the beginning so the last case, jump == 0, doesn't
        // change pos and we know exactly where to start after the loop.
        jump /= 2;
        if (dualFitness.evaluateMatlab(chromosomes.getChromosome(pos)) == Double.MAX_VALUE){
          pos -= jump;
        }
        else{
          pos += jump;
        }
      }

      if (((GeneralFormGene) chromosomes.getChromosome(pos).getGene(0)).getFitness() == Double.MAX_VALUE){
        pos--;
      }

      // Evaluate fitnesses as appropriate based on location.
      for (int i = pos; i >= 0; --i){
        dualFitness.evaluateMatlab(chromosomes.getChromosome(i));
      }
      for (int i = pos + 1; i < popSize; ++i){
        ((GeneralFormGene) chromosomes.getChromosome(i).getGene(0)).setFitness(Double.MAX_VALUE);
      }
    }
    */

    Collections.sort(chromosomes.getChromosomes(), fitnessComparator);

    howMany = (int) Math.round((howMany > popSize ? popSize : howMany) * pct);

    int previous = -1, offset = 0;
    for (int i = 0; i < howMany; ++i){
      int which = (int) Math.round(popSize * (Math.exp(bias * i / howMany) - 1) / (Math.exp(bias) - 1)) + offset;
      if (previous == which){
        offset++;
        which++;
      }
      previous = which;
      IChromosome selectedChromosome = chromosomes.getChromosome(which);
      selectedChromosome.setIsSelectedForNextGeneration(true);
      toPop.addChromosome(selectedChromosome);
    }
  }
}