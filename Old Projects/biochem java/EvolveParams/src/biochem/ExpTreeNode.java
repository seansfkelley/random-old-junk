package biochem;

import java.util.*;

// Replace this with a stack-like list?
// Fewer objects allocated; iterative instead of recursive.

public class ExpTreeNode{
  public static enum Operator {ZERO, ONE, METABOLITE, PARAMETER, ADD, MULTIPLY, DIVIDE, EXPONENT};

  private Operator op;
  private boolean binary;
  private ArrayList<ExpTreeNode> children;
  private int[] indices;
  private int which; // Holds metabolite or matrix index, as appropriate.

  public ExpTreeNode(Operator operator){
    op = operator;
    if (op == Operator.DIVIDE || op == Operator.EXPONENT){
      binary = true;
    }
    else{
      binary = false;
    }
    children = new ArrayList<ExpTreeNode>(2);
  }

  public ExpTreeNode(int which_metabolite){
    op = Operator.METABOLITE;
    which = which_metabolite;
  }

  public ExpTreeNode(int[] matrix_indices, int matrix_number){
    op = Operator.PARAMETER;
    indices = Arrays.copyOf(matrix_indices, matrix_indices.length);
    which = matrix_number;
  }

  public Operator getType(){
    return op;
  }

  public void addChild(ExpTreeNode node){
    if (op == Operator.ZERO || op == Operator.ONE ||  op == Operator.METABOLITE || op == Operator.PARAMETER){
      throw new IllegalStateException("Cannot add children to this type of node.");
    }
    else if (binary && children.size() == 2){
      throw new IllegalStateException("Binary node already has two children.");
    }

    children.add(node);
  }

  public int numChildren(){
    return children == null ? 0 : children.size();
  }

  public ExpTreeNode getChild(int which){
    if (op == Operator.ZERO || op == Operator.ONE || op == Operator.METABOLITE || op == Operator.PARAMETER){
      throw new IllegalStateException("Leaf nodes have no children.");
    }
    return children.get(which);
  }

  public double evaluate(SparseMultiMatrix[] matrices, double[] concs){
    switch(op){
      case ZERO:
        return 0;
      case ONE:
        return 1;
      case METABOLITE:
        return concs[which];
      case PARAMETER:
        return matrices[which].get(indices) / GAParameters.DENOMS_D[which];
      case ADD:
        double sum = 0;
        for (int i = 0; i < children.size(); ++i){
          sum += children.get(i).evaluate(matrices, concs);
        }
        return sum;
      case MULTIPLY:
        double product = 1;
        for (int i = 0; i < children.size(); ++i){
          product *= children.get(i).evaluate(matrices, concs);
        }
        return product;
      case DIVIDE:
        return children.get(0).evaluate(matrices, concs) / children.get(1).evaluate(matrices, concs);
      case EXPONENT:
        // The parameters need not be checked because by definition the base is
        // a positive floating-point, and thus the exponent can be anything and
        // the expression will not fail.
        return Math.pow(children.get(0).evaluate(matrices, concs), children.get(1).evaluate(matrices, concs));
    }
    assert(false) : "Switch statement doesn't cover all cases!";
    return 0;
  }

  public String evaluateAsString(SparseMultiMatrix[] matrices){
    String temp;
    switch(op){
      case ZERO:
        return "0";
      case ONE:
        return "1";
      case METABOLITE:
        // +1 to make indices one-indexed as they appear almost everywhere else.
        return "X(" + (which + 1) + ")";
      case PARAMETER:
        return Double.toString(matrices[which].get(indices) / GAParameters.DENOMS_D[which]);
      case ADD:
        temp = "(";
        for (int i = 0; i < children.size(); ++i){
          temp += children.get(i).evaluateAsString(matrices) + " + ";
        }
        return temp.substring(0, temp.length() - 3) + ")";
      case MULTIPLY:
        temp = "(";
        for (int i = 0; i < children.size(); ++i){
          temp += children.get(i).evaluateAsString(matrices) + " * ";
        }
        return temp.substring(0, temp.length() - 3) + ")";
      case DIVIDE:
        return "(" + children.get(0).evaluateAsString(matrices) + " / " + children.get(1).evaluateAsString(matrices) + ")";
      case EXPONENT:
        return "(" + children.get(0).evaluateAsString(matrices) + " ^ " + children.get(1).evaluateAsString(matrices) + ")";
    }
    throw new IllegalStateException("Operator is not of a defined type?");
  }

  public void swapParameters(SparseMultiMatrix[] this_matrices,
                             ExpTreeNode other,
                             SparseMultiMatrix[] other_matrices){
    switch(op){
      case ZERO:
      case ONE:
      case METABOLITE:
        return;
      case PARAMETER:
        assert(which == other.which && indices == other.indices);
        int temp = this_matrices[which].get(indices);
        this_matrices[which].put(other_matrices[which].get(indices), indices);
        other_matrices[which].put(temp, indices);
        return;
      case ADD:
      case MULTIPLY:
      case DIVIDE:
      case EXPONENT:
        for (int i = 0; i < numChildren(); ++i){
          getChild(i).swapParameters(this_matrices, other.getChild(i), other_matrices);
        }
        return;
    }
    throw new IllegalStateException("Operator is not of a defined type?");
  }
}
