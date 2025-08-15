import pathlib as pl
import traceback

import dakota.environment as dakenv

script_dir = pl.Path(__file__).parent


def evaluate(x: float, y: float, z: float, i: int) -> tuple[float, float]:
    # Objective 1: Minimize the sum of squares
    obj1 = (x**2 + y**2 + z**2) ** i

    # Objective 2: Maximize the product
    obj2 = -(x * y * z)  # Negated because we conventionally minimize

    return obj1, obj2


def evaluator(inputs: dict) -> dict:
    try:
        # Get the continuous variables out of the input provided by dakota
        continous_values = inputs["cv"]
        continous_labels = inputs["cv_labels"]
        continous_inputs = {
            label: value for label, value in zip(continous_labels, continous_values)
        }
        discrete_values = inputs["div"]
        discrete_labels = inputs["div_labels"]
        discrete_inputs = {
            label: value for label, value in zip(discrete_labels, discrete_values)
        }

        # Put the objective in the dakota 'fns' field of the output
        outputs = {"fns": evaluate(**continous_inputs, **discrete_inputs)}
        return outputs
    except Exception as e:
        print(traceback.format_exc())
        raise (e)


def main() -> None:
    print("Starting dakota")

    dakota_conf_path = script_dir / "moga.in"
    dakota_conf = dakota_conf_path.read_text()
    study = dakenv.study(
        callbacks={"evaluator": evaluator},
        input_string=dakota_conf,
    )

    study.execute()


if __name__ == "__main__":
    main()
