
Some investigation into rules-engines in python
---

A DSL that allows rules to be defined in a semi-natural language:

`
 if name == "AAAA" require (retained >= 0 and retained < 10)`

Using the python rules engine package makes this easy to implement.

Discussion 
-
Martin Fowler has an interesting take on [rules-engines](https://martinfowler.com/bliki/RulesEngine.html). I think it's fair to say he's not entirely enthusiastic, for interesting reasons. 

I can certainly see the opportunity for emerging complexity. Complexity of all kinds is bad, but the type that creeps up over time is especially annoying. Keeping a system of rules managable and 
easy to reason about 
over a longer timeframe is obviously a great virtue. 

However, I can imagine applications with a smaller number of non-chained rules that I'd say gain from a rules-engine approach.

I see a 'business-readable' set of rules to be a great benefit; especially when the business is fine-tuning the rules and even the data model over time.

There's also the case of versioning and supporting client-specific rules - a lot easier if they're in a common DDD ubiquitous language.

I wonder why he didn't suggest a set of reference cases (eg tests) to verify the rules are operating as expected. TDD and being right up his street.

Obviously - 'is a rule engine suitable for my use case?' has the answer: 'It depends!'. I guess there could be a set of rules to answer that question.