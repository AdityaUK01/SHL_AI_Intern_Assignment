from evaluation.evaluator import SHLEvaluator

evaluator = SHLEvaluator()

reply = """
Java 8 is recommended together with
Core Java.
"""

recommendations = [

    {
        "name": "Java 8"
    },

    {
        "name": "Core Java"
    }

]

metrics = evaluator.evaluate(

    reply,

    recommendations,

    [

        "Java"

    ]

)

print(metrics)