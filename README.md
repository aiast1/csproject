# MPPI Voice Leading Solver


A Python system that takes a soprano melody and outputs a complete SATB (soprano, alto, tenor, bass) using Model Predictive Path Integral (MPPI) control. Instead of hard constraint trees we make the problem as a trajectory optimization: sample many possible futures, score them with a cost function (encoding music theory rules) and blend the best paths.
