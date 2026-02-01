from typing import Dict, Tuple


def bayes_update(prior: float, likelihood: float, evidence: float) -> float:

    if evidence == 0:
        return 0 # To avoid dividing by zero
    else:
        posterior = (likelihood * prior) / evidence # Bayes formula
        return posterior
    

def compute_evidence(prior: float, likelihood_h: float, likelihood_not_h: float) -> float:
    
    # Following the formula
    not_h = 1 - prior # Get not h value first
    evidence = (likelihood_h * prior) + (likelihood_not_h * not_h) # Evidence formula
    return evidence 


def update_belief_map(belief_map: Dict[Tuple[int, int], float],
                      sensor_reading: bool,
                      sensor_accuracy: float = 0.9) -> Dict[Tuple[int, int], float]:
    updated_belief_map = belief_map.copy() #Get a copy of current belief map
    for cell in belief_map: # Traverse map
        prior = belief_map[cell] # Get prior belief
        if(sensor_reading == True):
            likelihood = sensor_accuracy 
            not_likelihood = 1-sensor_accuracy
            # Getting likelihood and not likelihood values
        else:
            likelihood = 1-sensor_accuracy
            not_likelihood = sensor_accuracy
            # Getting likelihood and not likelihood values
        evidence = compute_evidence(prior,likelihood,not_likelihood) # Compute the evidence using the likelihood and not likelihood
        posterior = bayes_update(prior,likelihood,evidence) # Update prior using bayes update with the evidence
        updated_belief_map[cell] = posterior # Update the current cell's probabilty value
        # Go to next cell untill all is done 
    return updated_belief_map # Returns updated belief map of every cell with updated belief values

    
   

def sensor_model(actual_state: bool, sensor_accuracy: float = 0.9) -> Tuple[float, float]:
    
    if actual_state == True:  # obstacle exists
        return sensor_accuracy, 1 - sensor_accuracy
    else:  # no obstacle
        return 1 - sensor_accuracy, sensor_accuracy


# ============================================================================
# Testing Code
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Testing Bayesian Reasoning")
    print("=" * 60 + "\n")
    
    print("Example: Medical diagnosis")
    print("-" * 40)
    print("Disease prevalence: 1% (P(Disease) = 0.01)")
    print("Test accuracy: 95% (P(+|Disease) = 0.95)")
    print("False positive: 10% (P(+|Healthy) = 0.10)")
    print("\nPatient tests positive. What's the probability they have the disease?")
    
    try:
        # Prior
        P_disease = 0.01
        P_healthy = 1 - P_disease
        
        # Likelihood
        P_pos_given_disease = 0.95
        P_pos_given_healthy = 0.10
        
        # Evidence
        P_pos = compute_evidence(P_disease, P_pos_given_disease, P_pos_given_healthy)
        
        # Posterior
        P_disease_given_pos = bayes_update(P_disease, P_pos_given_disease, P_pos)
        
        print(f"\nResult: P(Disease|+) = {P_disease_given_pos:.1%}")
        print("(Surprisingly low despite positive test!)")
        
    except NotImplementedError:
        print("\n⚠️  Bayes' rule not implemented yet!")
    
    print("\n" + "=" * 60)
    print("  Example: Robot Sensor")
    print("=" * 60)
    print("\nRobot sensor is 90% accurate")
    print("Prior belief cell has obstacle: 30%")
    print("Sensor detects obstacle")
    print("\nWhat's updated belief?")
    
    try:
        P_obstacle = 0.30
        P_detect_if_obstacle = 0.90
        P_detect_if_free = 0.10
        
        P_detect = compute_evidence(P_obstacle, P_detect_if_obstacle, P_detect_if_free)
        P_obstacle_given_detect = bayes_update(P_obstacle, P_detect_if_obstacle, P_detect)
        
        print(f"\nResult: P(Obstacle|Detected) = {P_obstacle_given_detect:.1%}")
        print(f"Belief increased from {P_obstacle:.1%} to {P_obstacle_given_detect:.1%}")
        
    except NotImplementedError:
        print("\n⚠️  Bayes' rule not implemented yet!")
    
    print("\n💡 Tip: Start with the basic bayes_update() function,")
    print("   then build up to belief maps!")