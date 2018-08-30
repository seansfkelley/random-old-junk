package biochem;

import java.util.*;
import org.jgap.*;

public class GeneralFormSmallMutation extends BaseGeneticOperator{
  public int max_change,
             mutations;

  public GeneralFormSmallMutation(Configuration config, int maximum_mutation)
      throws InvalidConfigurationException{
    super(config);
    max_change = maximum_mutation;
    mutations = 1;
  }

  public GeneralFormSmallMutation(Configuration config, int maximum_mutation, int num_mutations)
      throws InvalidConfigurationException{
    super(config);
    max_change = maximum_mutation;
    mutations = num_mutations;
  }

  public int compareTo(Object o){
    GeneralFormSmallMutation other = (GeneralFormSmallMutation) o;
    return max_change - other.max_change;
  }

  // See GeneralFormCrossover for an explanation of this function. It has a
  // very similar structure.
  public void operate(Population a_population, List a_candidateChromosomes){
    ArrayList<IChromosome> members = new ArrayList<IChromosome>(a_population.size());
    for (Iterator i = a_population.iterator(); i.hasNext();) {
      members.add((IChromosome) i.next());
    }
    Comparator icc = new IChromosomeComparator();
    Collections.sort(members, icc);

    RandomGenerator rg = getConfiguration().getRandomGenerator();
    IChromosome member;
    GeneralFormGene gene;
    int total_mutations = (int) (Math.min(getConfiguration().getPopulationSize(), a_population.size()) * GAParameters.MEMBER_KEEP_RATE);
    for(int i = 0; i < total_mutations; ++i){
      member = a_population.getChromosome(i);
      gene = (GeneralFormGene) member.getGene(0);

      gene = gene.clone();

      for(int j = 0; j < mutations; ++j){
        gene.applyMutation(rg.nextInt(gene.size()), rg.nextInt(max_change), GAParameters.MutationType.ABSOLUTE);
      }

      try{
        a_candidateChromosomes.add(new Chromosome(getConfiguration(), new Gene[] {gene}));
      }
      catch (InvalidConfigurationException ice){
        GAMain.failWithError(ice);
      }
    }
  }

  public String toString(){
    return "Small mutation with Max Severity: " + max_change + "; Max Repetitions: " + mutations;
  }
}