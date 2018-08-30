package biochem;

import org.jgap.*;
import java.util.*;

public class GeneralFormDualFitness extends DataBasedFitnessFunction{
  private GeneralFormFitness gff_builtin;
  private GeneralFormMatlabFitness gff_matlab;
  private boolean use_matlab = false;
  private double last_average;

  public GeneralFormDualFitness(double[][] init_concs, GeneralFormGene gfg){
    gff_builtin = new GeneralFormFitness(init_concs);
    gff_matlab = new GeneralFormMatlabFitness(init_concs, gfg);
    last_average = -1;
  }

  // <editor-fold defaultstate="collapsed" desc="DataGeneratingFitnessFunction Interface">
  public void generateTestData(IChromosome a_subject) {
    gff_matlab.generateTestData(a_subject);
  }

  public void setTestData(double[][][] data, double[] delta_ts) {
    gff_builtin.setTestData(data, delta_ts);
  }

  // Not the most neatly organized function, oftentimes the adding to the
  // ArrayList and sorting will not be used. But it's a small performance hit,
  // and I don't feel like reworking the code. This is based off of a version
  // of the function that didn't have to deal with FITNESS_SWITCH_GENERATIONS.
  public void update(int generation, Population pop){
    if (use_matlab){
      return;
    }

    ArrayList<IChromosome> members = new ArrayList<IChromosome>(pop.size());
    for (Iterator i = pop.iterator(); i.hasNext();) {
      members.add((IChromosome) i.next());
    }
    Comparator icc = new IChromosomeComparator();
    Collections.sort(members, icc);

    if (GAParameters.FITNESS_SWITCH_GENERATIONS > 0){
      if (generation == GAParameters.FITNESS_SWITCH_GENERATIONS){
        use_matlab = true;
      }
    }
    else{
      // Only average the fittest MEMBER_KEEP_RATE percent.
      double avg = 0;
      int how_many = (int) (GAParameters.MEMBER_KEEP_RATE * GAParameters.POP_SIZE);
      for (int i = 0; i < how_many; ++i){
        avg += members.get(i).getFitnessValue();
      }
      avg /= how_many;

      if (last_average == -1){
        last_average = avg;
      }
      else{
        if (Math.abs((last_average / avg) - 1) < GAParameters.FITNESS_SWITCH_THRESHOLD){
          use_matlab = true;
        }
        else{
          last_average = avg;
        }
      }
    }

    if (use_matlab){
      for (Iterator i = members.iterator(); i.hasNext();){
        // OH GOD IT'S HIDEOUS
        // We have to reset all the fitnesses when we switch, since we're now
        // using a different grading scale.
        ((GeneralFormGene) ((IChromosome) i.next()).getGene(0)).setFitness(FitnessFunction.NO_FITNESS_VALUE);
      }
      List operators = members.get(0).getConfiguration().getGeneticOperators();
      for (Iterator i = operators.iterator(); i.hasNext();){
        BaseGeneticOperator op = (BaseGeneticOperator) i.next();
        if (op instanceof GeneralFormMutation){
          ((GeneralFormMutation) op).hillclimb_rate = GAParameters.MUTATION_SA_RATE;
        }
        else if (op instanceof GeneralFormSmallMutation){
          ((GeneralFormSmallMutation) op).mutations = GAParameters.MUTATION_SMALL_CHANGE_REPETITIONS;
        }
      }
    }
  }
  // </editor-fold>
  
  public double evaluate(IChromosome a_subject){
    return use_matlab ? gff_matlab.evaluate(a_subject) : gff_builtin.evaluate(a_subject);
  }

  public double evaluateBuiltin(IChromosome a_subject){
    return gff_builtin.evaluate(a_subject);
  }

  public double evaluateMatlab(IChromosome a_subject){
    return gff_matlab.evaluate(a_subject);
  }

  public boolean usingMatlab(){
    return use_matlab;
  }

  public String toString(){
    String s = "";
    if (GAParameters.FITNESS_SWITCH_GENERATIONS > 0){
      s += "Fitness switch generations: " + GAParameters.FITNESS_SWITCH_GENERATIONS + "\n";
    }
    else{
      s += "Fitness switch threshold: " + (GAParameters.FITNESS_SWITCH_THRESHOLD * 100) + "%\n";
    }
    return s + gff_builtin.toString() + '\n' + gff_matlab.toString();
  }
}