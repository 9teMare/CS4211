### Pseudocode for preprocessing

```
for season in seasons:
    for match in season:
        home_model = gen_model(match_url) # done
        home_prob = gen_prob(home_model) # zi hao and i doing

        away_model = gen_model(match_url) # done
        away_prob = gen_prob(away_model) # zi hao and i doing

        match_prob = softmax(home_prob, away_prob) # todo

        append match_url, match_prob to new_probabilities
```
