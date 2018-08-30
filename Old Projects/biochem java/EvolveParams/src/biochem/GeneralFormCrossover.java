package biochem;

import java.util.*;
import org.jgap.*;

public class GeneralFormCrossover extends BaseGeneticOperator{
  public double rate;
  public boolean is_dynamic;

  public GeneralFormCrossover(Configuration config, double crossover_rate)
      throws InvalidConfigurationException{
    super(config);
    rate = crossover_rate;
    is_dynamic = false;
  }

  public GeneralFormCrossover(Configuration config, double crossover_rate, boolean dynamic)
      throws InvalidConfigurationException{
    super(config);
    rate = crossover_rate;
    is_dynamic = true;
  }

  public int compareTo(Object o){
    GeneralFormCrossover other = (GeneralFormCrossover) o;
    if (is_dynamic != other.is_dynamic){
      // false is "less than" true.
      return is_dynamic ? 1 : -1;
    }
    if (rate != other.rate){
      if (rate > other.rate){
        return 1;
      }
      return -1;
    }
    return 0;
  }

  // Heavily based on operate() from CrossoverOperator.java.
  public void operate(Population a_population, List a_candidateChromosomes){
    int size = Math.min(getConfiguration().getPopulationSize(), a_population.size());
    int crossovers = (int) (size * rate);

    double best_fit = Double.POSITIVE_INFINITY, worst_fit = Double.NEGATIVE_INFINITY;
    for (int i = 0; i < size; ++i){
      double fitness = Math.log10(a_population.getChromosome(i).getFitnessValueDirectly());
      if (fitness < best_fit){
        best_fit = fitness;
      }
      else if (fitness > worst_fit){
        worst_fit = fitness;
      }
    }

    double severity;
    RandomGenerator rg = getConfiguration().getRandomGenerator();
    IChromosome member1, member2;
    GeneralFormGene gene1, gene2;
    for (int i = 0; i < crossovers; ++i){
      member1 = a_population.getChromosome(rg.nextInt(size));
      member2 = a_population.getChromosome(rg.nextInt(size));
      gene1 = (GeneralFormGene) member1.getGene(0);
      gene2 = (GeneralFormGene) member2.getGene(0);
      if ((member1.getAge() < 1 && member2.getAge() < 1) || gene1.equals(gene2)){
        continue;
      }
      // Enforce deep cloning of the genes in question. a_population is a bunch
      // of IChromosomes, which guarantee nothing about the deepness of their
      // cloning.

      // No constraint implemented.

      gene1 = gene1.clone();
      gene2 = gene2.clone();
      // Apply each type with equal probability. Improvement: have modifiable
      // probabilities for each.
      int index;
      if (is_dynamic){
        severity = (Math.log10(member1.getFitnessValueDirectly()) - best_fit)
               / (worst_fit - best_fit) * GAParameters.CROSSOVER_DFR_EXTENSION;
        
        // Clamp chance to [0, 1].
        // Kind of a hacky solution to use 0.999. The problem is that both
        // endpoints of the range are inclusive, when the high end should be
        // exclusive (since it acts as an index).
        severity = severity >= 1.0 ? 0.999d : (severity < 0.0 ? 0.0 : severity);
        // Higher chance -> larger crossover. If/when different proabilities are
        // implemented, change the selection method here.
        index = (int) (severity * GAParameters.CrossoverType.values().length);
      }
      else{
        index = rg.nextInt(GAParameters.CrossoverType.values().length);
      }

      gene1.applyCrossover(gene2, GAParameters.CrossoverType.values()[index]);

      IChromosome[] children = OperatorTallies.compareAndTallyCrossover(member1, member2, gene1, gene2, index);

      a_candidateChromosomes.add(children[0]);
      a_candidateChromosomes.add(children[1]);
    }
  }

  public String toString(){
    return "Crossover rate: " + rate + " (" + (is_dynamic ? "dynamic" : "random") + " severity)\n" +
           "Range compression: " + GAParameters.CROSSOVER_DFR_EXTENSION;
  }
}
