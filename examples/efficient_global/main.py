import pathlib as pl

import dakota.environment as dakenv
import numpy as np

script_dir = pl.Path(__file__).parent


def evaluator(inputs):
    # Get the continuous variables out of the input provided by dakota
    x,y = inputs["cv"]

    z = 2.5*np.exp(-1*(x**2 + y**2))*(x + y**2 + np.random.normal(0, 0.1, 1))
    print(f"Evaluated {x},{y}: {z}")
    
    # Put the objective in the dakota 'fns' field of the output
    outputs = {"fns": z}

    return outputs

def map_evaluator(map_inputs):

    return map(evaluator, map_inputs)

def main():
    print("Starting dakota")

    dakota_conf_path = script_dir / "efficient_global.in"
    dakota_conf = dakota_conf_path.read_text()
    study = dakenv.study(
        callbacks={"evaluator": map_evaluator},
        input_string=dakota_conf,
    )

    study.execute()


if __name__ == "__main__":
    main()
