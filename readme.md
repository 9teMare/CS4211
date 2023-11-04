### Pseudocode for preprocessing

```
for season in seasons:
    for match in season:
        home_model = gen_model(match_url) # done
        home_prob = gen_prob(home_model) # to do

        away_model = gen_model(match_url) # done
        away_prob = gen_prob(away_model) # to do

        match_prob = softmax(home_prob, away_prob) # done

        append match_url, match_prob to new_probabilities # done
```
