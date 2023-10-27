#!/usr/bin/env python3

def generate_player_probLoseBall(attacker: dict, defender: dict, k: float=1.0, weights: dict=None) -> int:
  if weights is None:
    weights = {
      'w1': 1, 'w2': 1, 'w3': 1, 'w4': 1, 'w5': 1,
      'w6': 1, 'w7': 1, 'w8': 1, 'w9': 1, 'w10': 1,
    }
    
  D = (weights['w1'] * defender['mentality_interceptions'] +
      weights['w2'] * defender['defending_marking'] +
      weights['w3'] * defender['defending_standing_tackle'] +
      weights['w4'] * defender['defending_sliding_tackle'] +
      weights['w5'] * defender['power_strength']
      )

  A = (weights['w6'] * attacker['skill_dribbling'] +
        weights['w7'] * attacker['skill_ball_control'] +
        weights['w8'] * attacker['movement_agility'] +
        weights['w9'] * attacker['movement_balance'] +
        weights['w10'] * attacker['power_strength'])

  F = defender['mentality_aggression'] / (attacker['mentality_aggression'] +
                                          attacker['movement_balance'] +
                                          attacker['skill_ball_control'])
  
  denominator = A
  if denominator == 0:
    return 100
  
  return int(min(k * D / denominator * (1 - F), 1) * 100)