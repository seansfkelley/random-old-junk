package biochem;

import org.jgap.*;
import java.util.*;

public class IChromosomeComparator implements Comparator<IChromosome>{
  public IChromosomeComparator(){
    ;
  }

  public int compare(IChromosome o1, IChromosome o2){
    double order = o1.getFitnessValue() - o2.getFitnessValue();
    if (order < 0){
      return -1;
    }
    else if(order > 0){
      return 1;
    }
    return 0;
  }
}
