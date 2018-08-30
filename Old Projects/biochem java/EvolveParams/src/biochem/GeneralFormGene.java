package biochem;

import org.jgap.*;

public class GeneralFormGene extends BaseGene{
  private static final int ALPHA_I = 0, BETA_I = 1, GAMMA_I = 2, K_I = 3;

  private static final int LEFT = 0, RIGHT = 1; // For understandability in ExpTreeNode traversal.

  private int num_metabolites;
  private SparseMultiMatrix alpha, beta, gamma, k;
  private SparseMultiMatrix[] matrices; // For ease of use.
  private ExpTreeNode[] exp_tree_roots;
  private double fitness = FitnessFunction.NO_FITNESS_VALUE;


  public GeneralFormGene(Configuration config, int metabolites)
         throws InvalidConfigurationException{
    super(config);
    num_metabolites = metabolites;
  }

  @Override
  public GeneralFormGene newGene(){
    return (GeneralFormGene) newGeneInternal();
  }

  public int compareTo(Object o){
    SparseMultiMatrix[] other_matrices = ((GeneralFormGene) o).getAllele();

    int compare;
    for (int i = 0; i < 4; ++i){
      compare = matrices[i].compareTo(other_matrices[i]);
      if (compare != 0){
        return compare;
      }
    }

    return 0;
  }

  @Override
  public boolean equals(Object o){
    return compareTo(o) == 0;
  }

  @Override
  // It is not this function's responsibility to protect its matrices from modification.
  public SparseMultiMatrix[] getAllele(){
    return matrices;
  }

  protected Gene newGeneInternal(){
    try{
      GeneralFormGene gfg = new GeneralFormGene(getConfiguration(), num_metabolites);
      gfg.setAllele(getAllele());
      return gfg;
    }
    catch (InvalidConfigurationException ice){
      System.err.println(ice);
      return null;
    }
  }

  protected SparseMultiMatrix[] getInternalValue(){
    return new SparseMultiMatrix[] {alpha, beta, gamma, k};
  }

  public double[] evaluate(double[] concentrations){
    double[] dXdts = new double[exp_tree_roots.length];
    for (int i = 0; i < concentrations.length; ++i){
      dXdts[i] = exp_tree_roots[i].evaluate(matrices, concentrations);
    }
    return dXdts;
  }

  public String evaluateAsString(){
    String[] evaluated = new String[exp_tree_roots.length];
    for (int i = 0; i < exp_tree_roots.length; ++i){
      evaluated[i] = exp_tree_roots[i].evaluateAsString(matrices);
    }
    String complete = "";
    for (int i = 0; i < evaluated.length - 1; ++i){
      complete += GAParameters.MATLAB_VAR_ODE_PARAM + "(" + (i + 1) + ") = " + evaluated[i] + ";\n";
    }
    return complete + GAParameters.MATLAB_VAR_ODE_PARAM + "(" + evaluated.length + ") = " + evaluated[evaluated.length - 1] + ";";
  }

  private void constructExpressionTrees(){
    exp_tree_roots = new ExpTreeNode[num_metabolites];
    for (int i = 0; i < num_metabolites; ++i){
      exp_tree_roots[i] = constructEquationNode(i);
    }
  }

  // <editor-fold defaultstate="collapsed" desc="constructExpressionTree private helper functions">
  // Optimization if necessary: retreive indices in sorted order, slice out the
  // appropriate section, and then pass in that section. That way each function
  // can slice it further, but also not worry about checking the more broad
  // indices (i.e. take out m, t, a from constructDenomTermNode and replace it
  // with an appropriately sliced int[][]).
  private ExpTreeNode constructEquationNode(int m) {
    ExpTreeNode equation_node = new ExpTreeNode(ExpTreeNode.Operator.ADD);

    int[][] all_indices = k.getIndices(true);
    int[] indices;
    int num_terms = -1;
    for (int i = 0; i < all_indices.length; ++i){
      indices = all_indices[i];
      if (indices[0] == m && indices[1] > num_terms) {
        num_terms = indices[1];
      }
    }
    num_terms++; // Want length, not last index.

    for (int i = 0; i < num_terms; ++i) {
      equation_node.addChild(constructTermNode(m, i));
    }

    if(equation_node.numChildren() == 0){
      equation_node = new ExpTreeNode(ExpTreeNode.Operator.ZERO);
    }

    return equation_node;
  }

  private ExpTreeNode constructTermNode(int m, int t) {
    ExpTreeNode term_node = new ExpTreeNode(ExpTreeNode.Operator.MULTIPLY);
    term_node.addChild(new ExpTreeNode(new int[]{m, t}, K_I));
    ExpTreeNode div_node = new ExpTreeNode(ExpTreeNode.Operator.DIVIDE);
    div_node.addChild(constructNumeratorNode(m, t));
    div_node.addChild(constructDenominatorNode(m, t));
    term_node.addChild(div_node);
    return term_node;
  }

  private ExpTreeNode constructNumeratorNode(int m, int t) {
    ExpTreeNode num_node = new ExpTreeNode(ExpTreeNode.Operator.MULTIPLY);
    
    ExpTreeNode temp_node;
    int[][] all_indices = gamma.getIndices(true);
    int[] indices;
    for (int i = 0; i < all_indices.length; ++i){
      indices = all_indices[i];
      if (indices[0] == m && indices[1] == t) {
        temp_node = new ExpTreeNode(ExpTreeNode.Operator.EXPONENT);
        temp_node.addChild(new ExpTreeNode(indices[2]));
        temp_node.addChild(new ExpTreeNode(indices, GAMMA_I));
        num_node.addChild(temp_node);
      }
    }

    if (num_node.numChildren() == 0){
      // Generate a placeholding node.
      num_node.addChild(new ExpTreeNode(ExpTreeNode.Operator.ONE));
    }

    return num_node;
  }

  private ExpTreeNode constructDenominatorNode(int m, int t) {
    ExpTreeNode denom_node = new ExpTreeNode(ExpTreeNode.Operator.ADD);

    int[][] all_indices = alpha.getIndices(true);
    int[] indices;
    int num_terms = -1;
    for (int i = 0; i < all_indices.length; ++i){
      indices = all_indices[i];
      if (indices[0] == m && indices[1] == t && indices[2] > num_terms) {
        num_terms = indices[2];
      }
    }
    num_terms++; // Want length, not last index.

    for (int i = 0; i < num_terms; ++i){
      denom_node.addChild(constructDenomTermNode(m, t, i));
    }

    if (denom_node.numChildren() == 0){
      // Generate a placeholding node.
      denom_node.addChild(new ExpTreeNode(ExpTreeNode.Operator.ONE));
    }

    return denom_node;
  }

  private ExpTreeNode constructDenomTermNode(int m, int t, int a){
    ExpTreeNode term_node = new ExpTreeNode(ExpTreeNode.Operator.MULTIPLY);

    ExpTreeNode exp_node, div_node;
    int[][] all_indices = alpha.getIndices(true);
    int[] indices;
    for (int i = 0; i < all_indices.length; ++i){
      indices = all_indices[i];
      if (indices[0] == m && indices[1] == t && indices[2] == a){
        div_node = new ExpTreeNode(ExpTreeNode.Operator.DIVIDE);
        div_node.addChild(new ExpTreeNode(indices[3]));
        div_node.addChild(new ExpTreeNode(indices, BETA_I));
        exp_node = new ExpTreeNode(ExpTreeNode.Operator.EXPONENT);
        exp_node.addChild(div_node);
        exp_node.addChild(new ExpTreeNode(indices, ALPHA_I));
        term_node.addChild(exp_node);
      }
    }

    return term_node;
  }
  // </editor-fold>

  public int getNumParameters(){
    return alpha.numTerms() + beta.numTerms() + gamma.numTerms() + k.numTerms();
  }

  public int getNumZeroODEs(){
    int i;
    for (i = 0; i < exp_tree_roots.length; ++i){
      if (exp_tree_roots[i].getType() == ExpTreeNode.Operator.ZERO){
        return exp_tree_roots.length - i;
      }
    }
    return 0;
  }

  public int getMatrixIndex(int index){
    int which_matrix;
    for (which_matrix = 0; which_matrix < 4; ++which_matrix){
      if (index >= matrices[which_matrix].numTerms()){
        index -= matrices[which_matrix].numTerms();
      }
      else{
        break;
      }
    }
    return which_matrix;
  }

  public void applyMutation(int index, double a_percentage){
    applyMutation(index, a_percentage, GAParameters.MutationType.RELATIVE);
  }

  public void applyMutation(int index, double a_percentage, GAParameters.MutationType type){
    int which_matrix;
    for (which_matrix = 0; which_matrix < 4; ++which_matrix){
      if (index >= matrices[which_matrix].numTerms()){
        index -= matrices[which_matrix].numTerms();
      }
      else{
        break;
      }
    }
    SparseMultiMatrix matrix = matrices[which_matrix];

    int[][] all_indices = matrix.getIndices(true);
    int[] indices = all_indices[index];
    int value = matrix.get(indices);

    switch(type){
      case RELATIVE:
        value *= a_percentage;
        break;
      case ABSOLUTE:
        value += a_percentage;
        break;
      case RANDOM:
        value = getConfiguration().getRandomGenerator().
              nextInt(GAParameters.MAXS[which_matrix] - GAParameters.MINS[which_matrix] + 1)
              + GAParameters.MINS[which_matrix];
        break;
    }

    // Clamp the value to the allowed range.
    if (value > GAParameters.MAXS[which_matrix]){
      value = GAParameters.MAXS[which_matrix];
    }
    else if (value < GAParameters.MINS[which_matrix]){
      value = GAParameters.MINS[which_matrix];
    }

    fitness = FitnessFunction.NO_FITNESS_VALUE;
    matrix.put(value, indices);
  }

  // This destroys self and other. Make copies first! All equations between two
  // genes must have the same /structure/, otherwise the operator performs
  // undefined behavior.
  public void applyCrossover(GeneralFormGene other, GAParameters.CrossoverType type){
    RandomGenerator rg = getConfiguration().getRandomGenerator();
    int which = rg.nextInt(exp_tree_roots.length);
    // A rather naïve implementation. Obviously, don't give it systems with
    // all zeroes or with no equations at all.
    while (exp_tree_roots[which].getType() == ExpTreeNode.Operator.ZERO){
      which = rg.nextInt(exp_tree_roots.length);
    }

    ExpTreeNode root1 = getExpTreeRoot(which), root2 = other.getExpTreeRoot(which);
    which = rg.nextInt(root1.numChildren());
    ExpTreeNode term1 = root1.getChild(which), term2 = root2.getChild(which);
    switch(type){
      case EQUATION:
        root1.swapParameters(matrices, root2, other.matrices);
        break;
      case TERM_K:
        term1.getChild(LEFT).swapParameters(matrices,
                                            term2.getChild(LEFT),
                                            other.matrices);
        // No break!
      case TERM:
        term1.getChild(RIGHT).swapParameters(matrices,
                                             term2.getChild(RIGHT),
                                             other.matrices);
        break;
      case NUMER_K:
        term1.getChild(LEFT).swapParameters(matrices,
                                            term2.getChild(LEFT),
                                            other.matrices);
        // No break!
      case NUMER:
        term1.getChild(RIGHT).getChild(LEFT).swapParameters(matrices,
                                                            term2.getChild(RIGHT).getChild(LEFT),
                                                            other.matrices);
        break;
      case DENOM_K:
        term1.getChild(LEFT).swapParameters(matrices,
                                            term2.getChild(LEFT),
                                            other.matrices);
        // No break!
      case DENOM:
        term1.getChild(RIGHT).getChild(RIGHT).swapParameters(matrices,
                                                             term2.getChild(RIGHT).getChild(RIGHT),
                                                             other.matrices);
        break;
      case DENOM_TERM:
        which = rg.nextInt(term1.getChild(RIGHT).getChild(RIGHT).numChildren());
        term1.getChild(RIGHT).getChild(RIGHT).getChild(which).swapParameters(matrices,
                                                                             term2.getChild(RIGHT).getChild(RIGHT).getChild(which),
                                                                             other.matrices);
    }

    fitness = FitnessFunction.NO_FITNESS_VALUE;
  }

  public void setToRandomValue(RandomGenerator a_numberGenerator){
    if (matrices == null){
      throw new UnsupportedOperationException("Attempted initialization of matrices with unspecified dimensions.");
    }
    SparseMultiMatrix matrix;
    int[][] all_indices;
    for (int i = 0; i < 4; ++i){
      matrix = matrices[i];
      all_indices = matrix.getIndices();
      for (int j = 0; j < all_indices.length; ++j){
        matrix.put(a_numberGenerator.nextInt(GAParameters.MAXS[i] - GAParameters.MINS[i] + 1) + GAParameters.MINS[i], all_indices[j]);
      }
    }

    fitness = FitnessFunction.NO_FITNESS_VALUE;
    constructExpressionTrees();
  }

  // Makes sure it has its own instance of the parameter.
  public void setAllele(Object a_newValue){
    SparseMultiMatrix[] new_matrices = (SparseMultiMatrix[]) a_newValue;
    alpha = new_matrices[0].clone();
    beta =  new_matrices[1].clone();
    gamma = new_matrices[2].clone();
    k =     new_matrices[3].clone();
    matrices = new SparseMultiMatrix[] {alpha, beta, gamma, k};

    fitness = FitnessFunction.NO_FITNESS_VALUE;
    constructExpressionTrees();
  }

  public ExpTreeNode getExpTreeRoot(int which){
    return exp_tree_roots[which];
  }

  public String getPersistentRepresentation(){
    throw new UnsupportedOperationException("Not implemented.");
  }

  public void setValueFromPersistentRepresentation(String a_representation){
    throw new UnsupportedOperationException("Not implemented.");
  }

  // In order for this to be accurate, unused terms must be removed any time the
  // form of the equation is changed.
  @Override
  public int size(){
    int size = 0;
    for (int i = 0; i < 4; ++i){
      size += matrices[i].numTerms();
    }
    return size;
  }

  @Override
  public GeneralFormGene clone(){
    return newGene();
  }

  public double getFitness(){
    return fitness;
  }

  public void setFitness(double f){
    fitness = f;
  }

  @Override
  public String toString(){
    return toString(false);
  }

  public String toString(boolean long_name){
    if (long_name){
      return  evaluateAsString();
    }
    return "GeneralFormGene(" + size() + ")";
  }
}