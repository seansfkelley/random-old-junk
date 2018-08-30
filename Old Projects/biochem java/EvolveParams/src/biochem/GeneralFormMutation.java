package biochem;

import java.util.*;
import org.jgap.*;

public class GeneralFormMutation extends BaseGeneticOperator{
  public double rate,
                hillclimb_rate;
  public boolean is_dynamic;

  public GeneralFormMutation(Configuration config, double mutation_rate)
      throws InvalidConfigurationException{
    super(config);
    rate = mutation_rate;
    is_dynamic = false;
    hillclimb_rate = 0;
  }

  public GeneralFormMutation(Configuration config, double mutation_rate, boolean dynamic)
      throws InvalidConfigurationException{
    super(config);
    rate = mutation_rate;
    is_dynamic = true;
    hillclimb_rate = 0;
  }

  public GeneralFormMutation(Configuration config, double mutation_rate, boolean dynamic, double hillclimb)
      throws InvalidConfigurationException{
    super(config);
    rate = mutation_rate;
    is_dynamic = true;
    hillclimb_rate = hillclimb;
  }

  public int compareTo(Object o){
    GeneralFormMutation other = (GeneralFormMutation) o;
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

  // See GeneralFormCrossover for an explanation of this function. It has a
  // very similar structure.
  public void operate(Population a_population, List a_candidateChromosomes){
    int size = Math.min(getConfiguration().getPopulationSize(), a_population.size());
    int mutations = (int) (size * rate);

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
    IChromosome member, newMember;
    GeneralFormGene gene;

//    if (hillclimb_rate != 0){
//      System.err.println("Beginning mutations with chance for SA...");
//    }

    for (int i = 0; i < mutations; ++i){
      member = a_population.getChromosome(rg.nextInt(size));
      gene = (GeneralFormGene) member.getGene(0);

      gene = gene.clone();
      if (rg.nextDouble() < hillclimb_rate){
        gene = quickSimulatedAnnealing(gene);

        newMember = OperatorTallies.compareAndTallyMutation(member, gene, GAParameters.MutationTypeNominal.ANNEAL.ordinal());
      }
      else if (rg.nextDouble() < GAParameters.MUTATION_RANDOM_RATE){
        gene.applyMutation(rg.nextInt(gene.size()), 0, GAParameters.MutationType.RANDOM);

        newMember = OperatorTallies.compareAndTallyMutation(member, gene, GAParameters.MutationTypeNominal.RANDOM.ordinal());
      }
      else if (is_dynamic){
        severity = (Math.log10(member.getFitnessValueDirectly()) - best_fit)
                 / (worst_fit - best_fit) * GAParameters.MUTATION_DFR_EXTENSION;
        // No maximum value.
        severity = (severity < 0.0 ? 0.0 : severity) *
                GAParameters.MUTATION_RANGE + GAParameters.MUTATION_BASELINE;
        // Rather than being negated, severity is sometimes flipped.
        if (rg.nextDouble() - 0.5 < 0){
          severity = 1 / severity;
        }
        gene.applyMutation(rg.nextInt(gene.size()), severity, GAParameters.MutationType.RELATIVE);

        newMember = OperatorTallies.compareAndTallyMutation(member, gene, GAParameters.MutationTypeNominal.RELATIVE_ERROR_BASED.ordinal());
      }
      else{
        severity = rg.nextDouble() * GAParameters.MUTATION_RANGE + GAParameters.MUTATION_BASELINE;

        if (rg.nextDouble() - 0.5 < 0){
          severity = 1 / severity;
        }
        gene.applyMutation(rg.nextInt(gene.size()), severity, GAParameters.MutationType.RELATIVE);

        newMember = OperatorTallies.compareAndTallyMutation(member, gene, GAParameters.MutationTypeNominal.RELATIVE_RANDOM.ordinal());
      }
      
      a_candidateChromosomes.add(newMember);
    }
  }

  // This mutates a single parameter in one direction only.
  private GeneralFormGene quickSimulatedAnnealing(GeneralFormGene gfg){
    RandomGenerator rg = getConfiguration().getRandomGenerator();
    FitnessFunction ff = getConfiguration().getFitnessFunction();
    int param_number = rg.nextInt(gfg.size());
    double param_denom = GAParameters.DENOMS_D[gfg.getMatrixIndex(param_number)];
    int jump_size = (int) (Math.signum(rg.nextDouble() - 0.5) * param_denom / 4);

    GeneralFormGene previous, current = gfg;
    IChromosome previous_ic, current_ic = null;
    
    try{
      current_ic = new Chromosome(getConfiguration(), new Gene[] {current});
    }
    catch (InvalidConfigurationException ice){
      GAMain.failWithError(ice);
    }

    // jump_size here is analoagous to temperature.

    for (int i = 0; i < 3; ++i){
      previous = current;
      current = current.clone();
      current.applyMutation(param_number, jump_size, GAParameters.MutationType.ABSOLUTE);
      
      previous_ic = current_ic;
      try{
        current_ic = new Chromosome(getConfiguration(), new Gene[] {current});
      }
      catch (InvalidConfigurationException ice){
        GAMain.failWithError(ice);
      }

      // If this is a good change, keep going with this size.
      if (ff.getFitnessValue(current_ic) < ff.getFitnessValue(previous_ic)){
        --i;
      }
      // If this is a bad change, revert and prepare for the next attempt.
      else{
        current = previous;
        current_ic = previous_ic;
        jump_size /= 2;
      }
    }

    return current;
  }

  public String toString(){
    return "Mutation rate: " + rate + " (" + (is_dynamic ? "dynamic" : "random") + " severity); Random mutation chance: " + GAParameters.MUTATION_RANDOM_RATE + ")\n" +
           "Hillclimb rate: " + hillclimb_rate + "; Range extension: " + GAParameters.MUTATION_DFR_EXTENSION + "; Baseline: " + GAParameters.MUTATION_BASELINE;
  }
}