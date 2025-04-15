# NuQes

## Installation

```
git submodule add https://github.com/sqrta/funsearch.git
pip install -r requirements.txt
```

You need to call your LLM by defining `class LLM._draw_sample(self, prompt: str) -> str` in `funsearch/implementation/sampler.py`, where `prompt` is the input to the LLM. Your `LLM._draw_sample` should return a valid pure python function in the python string format.

## Bivariate Bicycle Code Evaluation

We reuse the simulation software from [BCGMRY] Sergey Bravyi, Andrew Cross, Jay Gambetta, Dmitri Maslov, Patrick Rall, Theodore Yoder, High-threshold and low-overhead fault-tolerant quantum memory https://arxiv.org/abs/2308.07915. The original git repo is [here](https://github.com/sbravyi/BivariateBicycleCodes). The evaluation code is in the `BivariateBicycleCodes` folder

```
cd BivariateBicycleCodes
```

The simulation software consists of two python scripts:

set_decoder.py is the offline part of the decoder that constructs check matrices, syndrome measurement circuits, and decoding matrices for a particular quantum code. This computation can take a few minutes per code. All code data is saved to disk. One has to call decoder_setup.py only once for each combination (code, error rate, number of syndrome cycles).

decoder_run.py is the online part of the decoder that simulates error correction circuits. It relies on the software implementation of the Belief Propagation with the Ordered Statistics Decoder due to Joschka Roffe "LDPC: Python tools for low density parity check codes"

File naming: the working directory that contains decoder_setup.py and decoder_run.py must contain folders "TMP" and "CODE_n_k_d" for each code [[n,k,d]] to be simulated. Initially these folders are empty. Folder "TMP" stores code data files with check matrices, syndrome measurement circuits, and decoding matrices. There is a separate data file for each combination (code, error rate, number of syndrome cycles). Create code data files using decoder_setup.py. Folder "CODE_n_k_d" contains a file "result" that stores the simulation results. Each line in the "result" file has four columns: column 1: physical error rate, column 2: number of syndrome cycles, column 3: number of Monte Carlo trials, column 4: number of failed trials that resulted in a logical error. Each trial runs the noisy error correction circuit followed by a noiseless syndrome measurement of all stabilizers, decoding, and error correction. A trial is failed if error correction results in a non-identity logical Pauli error.

distance_test.py calculates the code distance by solving an integer linear program

run `python set_decoder_288.py` and `python set_decoder_170.py` to setup the decoder test for the [[288, 12, 22]] code and [[170, 16, 10]] code. Then run 
```
python decoder_run.py n k d [error_rate] [iterations]
``` 
to simulate the error of the [[n, k, d]] code. For example `python decoder_run.py 288 12 22 0.0035 10000` will simulate the logical error rate of the [[288, 12, 22]] code with base error 0.0035 for 10000 iterations. `python decoder_run.py 170 16 10 0.003 20000` will simulate the logical error rate of the [[170, 16, 10]] code with base error 0.0035 for 20000 iterations.

## Quantum Lego Codes Evaluation

We store the check matrix of all codes we list in the Table 2 under different noise model in the folder `QLegoCodes/foundBest`. To reproduce the result in Table 2, run the command below

```
cd QLegoCodes
python benchEval.py
```

## QECC Search with FunSearch

This repository leverages a customized fork of FunSearch, originally developed by Google DeepMind and available [here](https://github.com/google-deepmind/funsearch), to automate the search for effective heuristic functions in Bivariate Bicycle code discovery.

> **Reference:**
> Romera-Paredes, B. et al. [Mathematical discoveries from program search with large language models](https://www.nature.com/articles/s41586-023-06924-6). *Nature* (2023)

---

### How FunSearch Works

FunSearch integrates large language models (LLMs) with evolutionary algorithms to optimize program synthesis:

- **LLM as Program Sampler:**
The LLM generates new program variants based on provided prompts.
- **Evaluator Function:**
Each candidate program is scored using a user-defined evaluation function.
- **Evolutionary Loop:**
    - Top-performing programs are stored in a database.
    - The LLM creates new variants by combining or reworking the best candidates.
    - This process repeats until a stopping criterion is met (e.g., convergence or iteration limit).
- **Termination:**
After the specified number of iterations, the program with the highest score is selected as the result.

---

### Bivariate Bicycle Code Search Example

An example configuration for Bivariate Bicycle code search is provided in `BBcodeSearch/main.py`. This demonstrates how to set up FunSearch to evolve heuristic functions tailored for this problem.

```python
with open("skeleton.py", "r") as f:
    content = f.read()
    sandbox = Sandbox(score)
    databaseConf = ProgramsDatabaseConfig(num_islands=1)
    conf = Config(
        sandbox=sandbox,
        programs_database=databaseConf,
        init_template="init_template/",
        prompt_manipulate=prompt_manipulate,
        num_samplers=1,
        num_evaluators=1,
        samples_per_prompt=1,
        iterations=5,
    )
    inputs = [None]
    main(content, inputs, conf)
```


#### Key Components

- **`main` Function:**
Accepts three arguments:
    - `content`: The program skeleton to be evolved (should include a function decorated with `@funsearch.evolve`).
    - `inputs`: Input data for evaluation (can be `[None]` if not needed).
    - `conf`: Configuration object for FunSearch.
- **Sandbox (Evaluator):**
Defines how each candidate function is evaluated. The `score` function writes the candidate to `Priority.py`, runs `evalFunc.py`, and reads the resulting score from a file.

```python
def score(prog):
    with open("Priority.py", "w") as f:
        f.write(prog)
    os.system("python3 evalFunc.py")
    with open("result", "r") as f:
        res = f.read().rstrip()
        result = float(res)
    return result, True
```

- **ProgramsDatabaseConfig:**
Configures the program database, such as the number of islands (parallel search populations).
- **Prompt Manipulation:**
Allows customization of the prompt sent to the LLM. For example, you can prepend a custom prompt head:

```python
def prompt_manipulate(prompt):
    with open("prompt_head.txt", "r") as f:
        head = f.read()
    return head + "\n" + prompt
```

- **Iterations:**
Sets the number of evolutionary cycles before termination.
- **Optional: `init_template`:**
Specifies initial implementations to seed the search.

---

### Customization Tips

- To access the best program found in each island during the search, modify the `sample` method in the `Sampler` class (`funsearch/implementation/sampler.py`). Use:
    - `self._database._best_score_per_island[Island_index]`
    - `self._database._best_program_per_island[Island_index]`