package biochem;

import java.util.*;

// Implement a cleaner version.

/* A sparse, n-dimensional matrix implemented using a HashMap. It is not safe:
 * no checking of input indices is ever performed, but it will check to make
 * sure you supply the right number of dimensions.
 *
 * Notes:
 * The mat HashMap uses Integers for the keys rather than int[] because int[]
 * doesn't have it's own hashCode function - it uses Object's, and that uses
 * the object code. In short, two separate arrays that contain the same numbers
 * will map to two distinct values, and that's bad. So I manually call the
 * Arrays.hashCode() function that uses the contents of the arrays, and then
 * map based off its return value.
 *
 * Since the keys to the mat HashMap are now Integers and not int[], I must also
 * maintain a separate map that holds the outside-facing 'keys' for this map --
 * i.e. the int[]s.
 */

public class SparseMultiMatrix implements Comparable{
  private HashMap mat, keys;
  private int dims, denominator;
  private IntArrayComparator compare;

  public SparseMultiMatrix(int numDimensions){
    mat = new HashMap<Integer, Integer>();
    keys = new HashMap<Integer, int[]>();
    dims = numDimensions;
    compare = new IntArrayComparator();
    denominator = 1;
  }

  public SparseMultiMatrix(int numDimensions, int denom){
    mat = new HashMap<Integer, Integer>();
    keys = new HashMap<Integer, int[]>();
    dims = numDimensions;
    compare = new IntArrayComparator();
    denominator = denom;
  }

  public int get(int... indices){
    return ((Integer) mat.get(Arrays.hashCode(indices))).intValue();
  }

  public void put(double value, int... indices){
    assert (indices.length == dims) : "Indices have wrong dimensions.";
    Integer key = Arrays.hashCode(indices);
    mat.put(key, Integer.valueOf((int) (value * denominator)));
    keys.put(key, Arrays.copyOf(indices, indices.length));
  }

  public void put(int value, int... indices){
    assert (indices.length == dims) : "Indices have wrong dimensions.";
    Integer key = Arrays.hashCode(indices);
    mat.put(key, Integer.valueOf(value * denominator));
    keys.put(key, Arrays.copyOf(indices, indices.length));
  }

  public void remove(int[] indices){
    Integer key = Arrays.hashCode(indices);
    mat.remove(key);
    keys.remove(key);
  }

  public int numDimensions(){
    return dims;
  }

  public int numTerms(){
    return mat.size();
  }

  // This is a completely absurd workaround. Primitive arrays are objects, yet
  // trying:
  // int[][] all_indices = (int[][]) keys.values().toArray();
  // doesn't work because of ClassCastExceptions:
  // [Ljava.lang.Object; cannot be cast to [[I
  // But it's clearly a valid cast, since trying:
  // System.out.println(Arrays.deepToString(keys.values().toArray()));
  // functions exactly as expected. To top it off, even the for-loop workaround
  // isn't enough. Arrays.sort(all_indices); will also fail with a class cast
  // exception since int[]s apparently aren't Comparable. Java, why the hell
  // won't you just trust me when I tell you that IT'S A GODDAMN int[][] THAT'S
  // WHY I CASTED IT LIKE THAT
  public int[][] getIndices(boolean sorted){
    Object[] index_arrays = keys.values().toArray();
    int[][] all_indices = new int[index_arrays.length][0];
    for (int i = 0; i < index_arrays.length; ++i){
      all_indices[i] = (int[]) (index_arrays[i]);
    }
    if (sorted){
      Arrays.sort(all_indices, compare);
    }
    return all_indices;
  }

  public int[][] getIndices(){
    return getIndices(false);
  }

  public int[] randomIndices(){
    return (int[]) keys.values().toArray()[(int) (Math.random() * keys.size())];
  }

  public int compareTo(Object o){
    SparseMultiMatrix other = (SparseMultiMatrix) o;
    if (numTerms() != other.numTerms()){
      return numTerms() - other.numTerms();
    }

    int index_compare;
    int[][] self_indices = getIndices(true), other_indices = other.getIndices(true);
    for (int i = 0; i < self_indices.length; ++i){
      index_compare = IntArrayComparator.staticCompare(self_indices[i], other_indices[i]);
      if (index_compare != 0){
        return index_compare;
      }
      else if (get(self_indices[i]) != other.get(other_indices[i])){
        return get(self_indices[i]) - other.get(other_indices[i]);
      }
    }
    return 0;
  }

  @Override
  public SparseMultiMatrix clone(){
    SparseMultiMatrix new_matrix = new SparseMultiMatrix(dims);
    int[][] indices = getIndices(false);
    // No HashMap.clone()?
    for (int i = 0; i < indices.length; ++i){
      new_matrix.put(get(indices[i]), indices[i]);
    }
    return new_matrix;
  }
}