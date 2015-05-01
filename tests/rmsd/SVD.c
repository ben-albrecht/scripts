#include "molecule.h"
#include <armadillo>
#include "mytypes.h"
#include "COM.h"


/**
 @brief Translates a molecule to center-of-mass coordinates.
 */
void translateToCOM(Molecule& M)
{
  // Calculate C.O.M.
  arma::rowvec com(M.XYZ.n_cols);
  com.fill(0.0);
  double total_mass = 0.0;
  for (int i = 0; i < M.XYZ.n_rows; i++)
  {
    com += M.AtomicMasses(i) * M.XYZ.row(i);
    total_mass += M.AtomicMasses(i);
  }
  com /= total_mass;
  //arma::mat com = M.XYZ.row(0);

  for (int i = 0; i < M.XYZ.n_rows; i++)
  {
    M.XYZ.row(i) -= com;
  }
}

/**
 @brief Aligns two molecules such that the RMSD is minimized.
 */
void alignMolecules(Molecule& A, Molecule& B)
{
  arma::mat R = findRotationMatrix(A,B);

  // Rotate B into maximum overlap with A
  for (int i = 0; i < B.XYZ.n_rows; i++)
  {
    B.XYZ.row(i) = trans(R * trans(B.XYZ.row(i)));
  }
}

/**
 @brief Finds the rotation matrix that aligns two molecules
 */
arma::mat findRotationMatrix(const Molecule& A, const Molecule& B)
{
  const int d = A.XYZ.n_cols;
  arma::mat J(d,d);
  J.fill(0.0);

  // TODO: Check dimensions of matrices

  for (int i = 0; i < A.XYZ.n_rows; i++) {
    J += trans(A.XYZ.row(i)) * B.XYZ.row(i);
  }
  #ifdef DEBUG
  J.print("J:");
  #endif

  arma::colvec s;
  arma::mat U;
  arma::mat V;
  svd(U,s,V,J);

/*
  std::cout << "SVD:   J = (U) (s) (V^T)" << std::endl;
  U.print("U:");
  s.print("s:");
  V.print("V:");
*/

  arma::mat R = trans(V * trans(U));
  #ifdef DEBUG
  R.print("R:");
  #endif

  return R;
}
