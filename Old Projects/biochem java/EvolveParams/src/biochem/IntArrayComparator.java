package biochem;

import java.util.*;

public class IntArrayComparator implements Comparator{
  public IntArrayComparator(){}
  public int compare(Object o1, Object o2){
    return IntArrayComparator.staticCompare(o1, o2);
  }

  // There's really no reason to actually instantiate an object when doing a
  // comparison, since no state is saved. So I present this option as well.
  public static int staticCompare(Object o1, Object o2){
    int[] a1 = (int[]) o1, a2 = (int[]) o2;
    if(a1.length != a2.length){
      return a1.length - a2.length;
    }
    for (int i = 0; i < a1.length; ++i){
      if (a1[i] != a2[i]){
        return a1[i] - a2[i];
      }
    }
    return 0;
  }

  public boolean equals(Object other){
    return super.equals(other);
  }
}
