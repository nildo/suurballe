set N;
set A within N cross N;
set S{i in N}:={j in N: (i,j) in A}; # Successors
set P{i in N}:={j in N: (j,i) in A}; # Predecessors

param c{A};         # Capacity
param a{A};         # Cost
param r{N};         # Flow required

var f{A} >= 0;      # Flow

minimize obj: sum{(i,j) in A} a[i,j] * f[i,j];

# Capacity Constraint:
s.t. cc{(i,j) in A}: f[i,j] <= c[i,j];
# Flow Conservation:
s.t. fc{i in N}:     sum{j in S[i]} f[i,j] - sum{j in P[i]} f[j,i] = r[i];

end;
