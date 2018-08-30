package biochem;

import org.jgap.*;

public class OperatorTallies{
  public static int[] crossover_good = new int[GAParameters.CrossoverType.values().length];
  public static int[] crossover_bad = new int[GAParameters.CrossoverType.values().length];

  public static int[] mutation_good = new int[GAParameters.MutationTypeNominal.values().length];
  public static int[] mutation_bad = new int[GAParameters.MutationTypeNominal.values().length];
  

  public static IChromosome compareAndTallyMutation(IChromosome originalChromosome, GeneralFormGene mutatedGene, int tallyIndex){
    IChromosome mutatedChromosome = null;

    try{
      mutatedChromosome = new Chromosome(mutatedGene.getConfiguration(), new Gene[] {mutatedGene});
    }
    catch (InvalidConfigurationException ice){
      GAMain.failWithError(ice);
    }

    if (mutatedChromosome.getFitnessValue() < originalChromosome.getFitnessValue()){
      mutation_good[tallyIndex]++;
    }
    else{
      mutation_bad[tallyIndex]++;
    }

    return mutatedChromosome;
  }

  public static IChromosome[] compareAndTallyCrossover(IChromosome parentChromosome1, IChromosome parentChromosome2, GeneralFormGene childGene1, GeneralFormGene childGene2, int tallyIndex){
    IChromosome childChromosome1 = null, childChromosome2 = null;

    try{
      childChromosome1 = new Chromosome(childGene1.getConfiguration(), new Gene[] {childGene1});
      childChromosome2 = new Chromosome(childGene2.getConfiguration(), new Gene[] {childGene2});
    }
    catch (InvalidConfigurationException ice){
      GAMain.failWithError(ice);
    }

    IChromosome[] children = new IChromosome[] {childChromosome1, childChromosome2},
                  parents =  new IChromosome[] {parentChromosome1, parentChromosome2};

    for (IChromosome child : children){
      for (IChromosome parent : parents){
        if (child.getFitnessValue() < parent.getFitnessValue()){
          crossover_good[tallyIndex]++;
        }
        else{
          crossover_bad[tallyIndex]++;
        }
      }
    }

    return children;
  }

  public static void printTallies(){
    GAMain.statusMessage("Mutation Tallies (Name Good/Bad):", 1);

    for (GAParameters.MutationTypeNominal t : GAParameters.MutationTypeNominal.values()){
      GAMain.statusMessage(t.toString() + ": " + mutation_good[t.ordinal()] + "/" + mutation_bad[t.ordinal()], 1);
    }

    GAMain.statusMessage("Crossover Tallies (Name Good/Bad):", 1);

    for (GAParameters.CrossoverType t : GAParameters.CrossoverType.values()){
      GAMain.statusMessage(t.toString() + ": " + crossover_good[t.ordinal()] + "/" + crossover_bad[t.ordinal()], 1);
    }
  }
}